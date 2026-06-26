# PINN 机制函数模板（PINN Mechanism Templates）

> **配合**: `component-specs.md` §2.4
> **作用**: 按物理域提供 PINN 机制函数的网络架构、物理约束 loss、训练循环模板

---

## 一、PINN 在 CDA 中的角色

CDA 的机制函数有两种实现方式：

| 方式 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| **物理公式** | 已知物理定律 | 精确、可解释、零训练 | 需要领域知识 |
| **PINN 学习** | 未知或复杂机制 | 通用、数据驱动 | 需要训练、黑箱 |

**CDA 的设计偏好**：优先使用物理公式，PINN 作为补充（用于物理公式无法覆盖的子过程）。

```
典型混合方案：
  已知边 → ThermalConduction（傅里叶定律）
  未知边 → PINNMechanism（从数据学习）
  在线精化 → 物理公式 + PINN 残差修正
```

---

## 二、热力学 PINN 模板

### 2.1 纯热传导学习

**场景**：已知存在热传导关系，但等效传热系数 k_eff 未知（材料老化、接触热阻等）。

```python
class ThermalPINN(nn.Module):
    """学习热传导的等效机制函数。
    
    输入：[T_src, T_tgt, dT/dt_src, dT/dt_tgt, distance, area]
    输出：Q_dot（热流率 W）
    
    物理约束：
    1. 因果方向：T_src > T_tgt → Q > 0
    2. 线性近似：Q ≈ k_eff · A/d · ΔT（PINN 应在大范围内逼近此形式）
    """
    
    def __init__(self, hidden_dims=[64, 64, 32]):
        super().__init__()
        # 输入：6 维
        in_dim = 6
        layers = []
        prev = in_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.Tanh()])
            prev = h
        layers.append(nn.Linear(prev, 1))  # 输出：热流率标量
        self.net = nn.Sequential(*layers)
        
        # 初始化为小输出
        self._init_small()
    
    def _init_small(self):
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight, gain=0.01)
                nn.init.zeros_(m.bias)
    
    def forward(self, T_src, T_tgt, dT_src, dT_tgt, dist, area):
        x = torch.stack([T_src, T_tgt, dT_src, dT_tgt, dist, area], dim=-1)
        return self.net(x).squeeze(-1)


class ThermalPINNLoss(nn.Module):
    """热力学 PINN 的物理约束 loss。
    
    Loss = L_data + λ₁·L_physics + λ₂·L_monotonicity + λ₃·L_energy
    """
    
    def __init__(self, lambda_physics=1.0, lambda_mono=10.0, lambda_energy=5.0):
        super().__init__()
        self.lam_phy = lambda_physics
        self.lam_mono = lambda_mono
        self.lam_ene = lambda_energy
    
    def forward(self, model, batch):
        """计算总 loss。
        
        batch 含：
          T_src, T_tgt: 温度
          Q_obs: 观测热流（用于 L_data）
          T_tgt_next: 下一时刻 target 温度（用于物理约束）
          mass, specific_heat: target 属性（用于能量平衡）
          dt: 时间步长
        """
        T_src, T_tgt = batch['T_src'], batch['T_tgt']
        Q_pred = model(T_src, T_tgt, 
                       batch.get('dT_src', torch.zeros_like(T_src)),
                       batch.get('dT_tgt', torch.zeros_like(T_tgt)),
                       batch['distance'], batch['area'])
        
        # L_data: MSE with observations
        L_data = F.mse_loss(Q_pred, batch['Q_obs'])
        
        # L_physics: 能量平衡
        # Q_in = m·C·dT/dt（流入 target 的热量 = 温升所需热量）
        Q_in = Q_pred * batch['dt']
        dT = batch['T_tgt_next'] - T_tgt
        Q_expected = batch['mass'] * batch['specific_heat'] * dT
        L_physics = F.mse_loss(Q_in, Q_expected)
        
        # L_monotonicity: 热从高温流向低温
        dT = T_src - T_tgt
        # Q 和 dT 应该同号
        violation = torch.relu(-Q_pred * dT)  # 违反时 > 0
        L_monotonicity = violation.mean()
        
        # L_energy: 对称性（交换 src/tgt 改变符号）
        if 'T_src_swap' in batch:
            Q_swap = model(batch['T_src_swap'], batch['T_tgt_swap'],
                          batch.get('dT_tgt', torch.zeros_like(T_tgt)),
                          batch.get('dT_src', torch.zeros_like(T_src)),
                          batch['distance'], batch['area'])
            L_energy = F.mse_loss(Q_pred, -Q_swap)
        else:
            L_energy = torch.tensor(0.0)
        
        total = (L_data 
                 + self.lam_phy * L_physics 
                 + self.lam_mono * L_monotonicity 
                 + self.lam_ene * L_energy)
        
        return total, {
            'data': L_data.item(),
            'physics': L_physics.item(),
            'monotonicity': L_monotonicity.item(),
            'energy': L_energy.item(),
        }
```

### 2.2 训练循环模板

```python
def train_thermal_pinn(model, loss_fn, train_loader, 
                       n_epochs=1000, lr=1e-3):
    """标准 PINN 训练循环。"""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, n_epochs)
    
    history = []
    for epoch in range(n_epochs):
        model.train()
        epoch_losses = {'data': 0, 'physics': 0, 'monotonicity': 0, 'energy': 0}
        
        for batch in train_loader:
            total_loss, loss_dict = loss_fn(model, batch)
            
            optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            for k, v in loss_dict.items():
                epoch_losses[k] += v
        
        scheduler.step()
        
        # 记录
        n = len(train_loader)
        history.append({k: v/n for k, v in epoch_losses.items()})
        
        if epoch % 100 == 0:
            print(f"Epoch {epoch}: "
                  f"data={epoch_losses['data']/n:.6f} "
                  f"phy={epoch_losses['physics']/n:.6f} "
                  f"mono={epoch_losses['monotonicity']/n:.6f}")
    
    return history
```

---

## 三、力学 PINN 模板

### 3.1 弹簧-阻尼学习

**场景**：已知存在弹性连接，但刚度和阻尼系数未知。

```python
class MechanicalPINN(nn.Module):
    """学习力学系统的力-位移关系。
    
    输入：[x_src, x_tgt, v_src, v_tgt, relative_distance]
    输出：F（作用在 target 上的力）
    
    物理约束：
    1. 牛顿第三定律：F_src→tgt = -F_tgt→src
    2. 能量守恒：弹性势能可积
    3. 因果方向：力趋向于减小偏差
    """
    
    def __init__(self, hidden_dims=[64, 32]):
        super().__init__()
        in_dim = 5
        layers = []
        prev = in_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.Tanh()])
            prev = h
        layers.append(nn.Linear(prev, 1))
        self.net = nn.Sequential(*layers)
        self._init_small()


class MechanicalPINNLoss(nn.Module):
    """力学 PINN 物理约束 loss。
    
    Loss = L_data + λ₁·L_newton3 + λ₂·L_energy_conservation + λ₃·L_dissipation
    """
    
    def __init__(self, lambda_newton3=10.0, lambda_energy=5.0, lambda_dissipation=1.0):
        super().__init__()
        self.lam_n3 = lambda_newton3
        self.lam_ene = lambda_energy
        self.lam_diss = lambda_dissipation
    
    def forward(self, model, batch):
        """
        batch 含：
          x_src, x_tgt: 位移
          v_src, v_tgt: 速度
          F_obs: 观测力
          mass: target 质量
          dt: 时间步长
          x_tgt_next, v_tgt_next: 下一时刻状态
        """
        x_src, x_tgt = batch['x_src'], batch['x_tgt']
        F_pred = model(x_src, x_tgt, batch['v_src'], batch['v_tgt'],
                       torch.abs(x_tgt - x_src))
        
        # L_data
        L_data = F.mse_loss(F_pred, batch['F_obs'])
        
        # L_newton3: 作用力 = 反作用力
        if 'x_src_swap' in batch:
            F_swap = model(batch['x_tgt'], batch['x_src'], 
                          batch['v_tgt'], batch['v_src'],
                          torch.abs(x_tgt - x_src))
            L_newton3 = F.mse_loss(F_pred, -F_swap)
        else:
            L_newton3 = torch.tensor(0.0)
        
        # L_energy: F = m·a → a = F/m → v_next = v + a·dt
        a = F_pred / batch['mass']
        v_pred = batch['v_tgt'] + a * batch['dt']
        L_energy = F.mse_loss(v_pred, batch['v_tgt_next'])
        
        # L_dissipation: 阻尼力方向与速度相反
        violation = torch.relu(F_pred * batch['v_tgt'])
        L_dissipation = violation.mean() * 0.1  # 弱约束（不是所有力学系统都有阻尼）
        
        total = (L_data + self.lam_n3 * L_newton3 
                 + self.lam_ene * L_energy + self.lam_diss * L_dissipation)
        
        return total, {
            'data': L_data.item(),
            'newton3': L_newton3.item(),
            'energy': L_energy.item(),
        }
```

---

## 四、通用 PINN 模板

### 4.1 无领域知识时的通用机制

**场景**：物理域未知、因果机制完全从数据学习。

```python
class GeneralPINN(nn.Module):
    """通用因果机制函数——无物理假设。
    
    输入：concat(full_state_source, full_state_target)
    输出：delta_state (dim_state,)
    
    物理约束：仅数据拟合 + 因果方向软约束
    """
    
    def __init__(self, state_dim: int, hidden_dims=[128, 64, 32],
                 residual: bool = False):
        """
        Args:
            state_dim: 单个实体的状态维度
            hidden_dims: 隐藏层尺寸
            residual: 是否使用残差连接（推荐 True）
        """
        super().__init__()
        in_dim = state_dim * 2
        out_dim = state_dim
        
        layers = []
        prev = in_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.GELU()])
            prev = h
        layers.append(nn.Linear(prev, out_dim))
        self.net = nn.Sequential(*layers)
        
        self.residual = residual
        self._init_small()
    
    def forward(self, s_src: torch.Tensor, s_tgt: torch.Tensor) -> torch.Tensor:
        x = torch.cat([s_src, s_tgt], dim=-1)
        out = self.net(x)
        if self.residual:
            out = out + s_tgt  # 残差：机制函数是状态的微扰
        return out
```

---

## 五、物理约束 Loss 设计指南

### 5.1 约束优先级矩阵

| 约束 | 优先级 | 权重范围 | 说明 |
|------|--------|---------|------|
| 数据拟合 L_data | 基础 | 1.0（基准） | 必须有，否则无法学习 |
| 守恒律（能量/动量） | 高 | 5.0 ~ 20.0 | 架构核心，不可违反 |
| 因果方向 | 高 | 10.0 ~ 50.0 | 热从高温到低温，力恢复平衡 |
| 对称性（牛顿第三定律） | 中 | 1.0 ~ 10.0 | 取决于物理域 |
| 因果延迟 | 低 | 0.1 ~ 1.0 | 弱约束，因为延迟可能由架构处理 |

### 5.2 权重调度策略

```python
class LossWeightScheduler:
    """训练过程中动态调整物理约束权重。
    
    策略：前期侧重数据拟合，后期加强物理约束。
    """
    
    def __init__(self, total_epochs, warmup_ratio=0.3):
        self.total_epochs = total_epochs
        self.warmup = int(total_epochs * warmup_ratio)
    
    def get_weights(self, epoch):
        if epoch < self.warmup:
            # 预热阶段：以数据拟合为主
            return {'data': 1.0, 'physics': 0.1, 'mono': 0.5}
        else:
            # 正式阶段：加强物理约束
            progress = (epoch - self.warmup) / (self.total_epochs - self.warmup)
            return {
                'data': 1.0,
                'physics': 0.1 + 9.9 * progress,      # 0.1 → 10.0
                'mono': 0.5 + 19.5 * progress,         # 0.5 → 20.0
            }
```

---

## 六、PINN 与物理公式的混合策略

### 6.1 残差修正

```python
class PhysicsPlusResidualPINN(MechanismFunction):
    """物理公式 + PINN 残差修正。
    
    f_total = f_physics + f_pinn_residual
    
    适用场景：物理公式大致正确但有系统性偏差。
    """
    
    def __init__(self, physics_fn: MechanismFunction, 
                 residual_dim: int, hidden_dims=[32, 16]):
        super().__init__("physics_plus_residual")
        self.physics = physics_fn
        self.residual_net = GeneralPINN(residual_dim, hidden_dims, residual=True)
    
    def forward(self, s_src, s_tgt):
        dq_phys, dp_phys = self.physics(s_src, s_tgt)
        dq_res = self.residual_net(s_src.full_state(), s_tgt.full_state())
        dim_q = s_tgt.q.shape[0]
        return dq_phys + dq_res[:dim_q], dp_phys + dq_res[dim_q:]
```

### 6.2 门控混合

```python
class GatedPhysicsPINN(MechanismFunction):
    """门控混合：物理公式和 PINN 通过学习到的权重混合。
    
    f_total = gate · f_physics + (1 - gate) · f_pinn
    
    gate 接近 1 → 信任物理公式
    gate 接近 0 → 信任 PINN
    """
    
    def __init__(self, physics_fn, pinn_fn, state_dim):
        super().__init__("gated_mixed")
        self.physics = physics_fn
        self.pinn = pinn_fn
        self.gate_net = nn.Sequential(
            nn.Linear(state_dim * 2, 16),
            nn.Sigmoid(),  # 输出 [0, 1]
        )
        # 初始化 gate ≈ 0.9（默认信任物理）
        nn.init.constant_(self.gate_net[0].weight, 0.0)
        nn.init.constant_(self.gate_net[0].bias, 2.0)  # sigmoid(2.0) ≈ 0.88
    
    def forward(self, s_src, s_tgt):
        x = torch.cat([s_src.full_state(), s_tgt.full_state()])
        gate = self.gate_net(x)
        
        dq_phys, dp_phys = self.physics(s_src, s_tgt)
        dq_pinn, dp_pinn = self.pinn(s_src, s_tgt)
        
        return (gate * dq_phys + (1 - gate) * dq_pinn,
                gate * dp_phys + (1 - gate) * dp_pinn)
```

---

## 七、训练数据准备

### 7.1 从 JSON 加载训练数据

```python
def prepare_training_data(graph_path: str, trajectory_path: str,
                          target_edge: Tuple[int, int],
                          window_size: int = 5):
    """从 CDA 合成数据准备 PINN 训练集。
    
    Args:
        graph_path: *.graph.json 路径
        trajectory_path: *.trajectory.json 路径
        target_edge: (source_id, target_id) 要学习的因果边
        window_size: 时间窗口大小（用于计算导数）
    
    Returns:
        dataset: 含 (features, targets) 的字典列表
    """
    trajectory = load_trajectory(trajectory_path)
    src_id, tgt_id = target_edge
    
    samples = []
    for i in range(len(trajectory) - window_size):
        src_states = [trajectory[i+j].get_entity(src_id) for j in range(window_size)]
        tgt_states = [trajectory[i+j].get_entity(tgt_id) for j in range(window_size)]
        
        # 数值微分
        dT_src = (src_states[-1].q[0] - src_states[0].q[0]) / (window_size * dt)
        
        samples.append({
            'T_src': src_states[0].q[0],
            'T_tgt': tgt_states[0].q[0],
            'dT_src': dT_src,
            'Q_obs': tgt_states[0].p[0],  # 热流作为目标
            'T_tgt_next': tgt_states[-1].q[0],
            'distance': ...,
            'area': ...,
            'mass': tgt_states[0].attributes['mass'],
            'specific_heat': tgt_states[0].attributes['specific_heat'],
            'dt': dt,
        })
    
    return samples
```
