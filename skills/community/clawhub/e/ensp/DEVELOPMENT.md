# eNSP Skill 开发日志

## 概述
这是一个为 AI Agent 创建 eNSP 网络拓扑文件的 Skill。

## 已完成功能

### 1. 格式分析
通过分析 eNSP 官方示例文件，掌握了 .topo 格式：
- 文件位置：`E:\files\eNSP\examples\`
- 分析了 10+ 个不同拓扑示例

### 2. 核心文件
- `SKILL.md` - Agent 技能说明
- `references/topo-reference.md` - 格式参考文档

### 3. 支持的设备类型
| 设备 | Model | 说明 |
|------|-------|------|
| 路由器 | AR201 | Ethernet x8 + Ethernet x1 |
| 路由器 | AR1220 | 2GE + 8Ethernet |
| 路由器 | AR2220 | GE x1 + GE x2 + Serial x2 |
| 路由器 | AR2240 | GE x1 + GE x2 |
| 路由器 | AR3260 | GE x1 + GE x2 |
| 路由器 | Router | Ethernet x2 + GE x4 + Serial x4 |
| 路由器 | NE40E/NE5000E/NE9000 | 10x Ethernet |
| 路由器 | R250D | GE x1 |
| 交换机 | S3700 | Ethernet x22 + GE x2 |
| 交换机 | S5700 | 24GE |
| 交换机 | CE6800 | 20x GE |
| 交换机 | CE12800 | 10x GE |
| 交换机 | CX | 10x Ethernet |
| 防火墙 | USG5500 | GE x9 |
| 防火墙 | USG6000V | GE x1 + GE x7 |
| 无线 AC | AC6005 | 8GE |
| 无线 AC | AC6605 | 24GE |
| 无线 AP | AP2xxx/AP4xxx/AP5xxx/AP6xxx/AP7xxx/AP8xxx/AP9xxx | 各型AP |
| LTE | AD9430 | 28GE |
| PC | PC | 1GE |
| 笔记本 | Laptop | 1GE |
| 服务器 | Server | 1Ethernet |
| 客户端 | Client | 1Ethernet |
| 组播服务器 | MCS | 1Ethernet |
| 云 | Cloud | Ethernet 接口 |
| 帧中继交换机 | FRSW | Serial x16 |
| 以太网HUB | HUB | Ethernet x16 |
| 无线终端 | STA | 无线 |
| 手机 | Cellphone | 无线 |

### 4. 支持的线缆类型
- `Copper` - 以太网线
- `Serial` - 串口线
- `Auto` - 自动检测

### 5. 支持的图形元素
- `shapes` - 区域框（type 0/1/2）
- `txttips` - 文本标注

## 待完成功能

### 设备支持
- [x] Server（服务器） - 已支持
- [x] 防火墙（USG5500、USG6000V） - 已支持
- [x] 更多的 AP 型号（AP2xxx、AP8xxx、AP9xxx系列） - 已支持
- [x] 更多的路由器型号（AR201、AR2240、AR3260） - 已支持
- [x] NE40E/NE5000E/NE9000 - 已支持
- [x] CE6800/CE12800 - 已支持
- [x] CX - 已支持
- [x] S3700 - 已支持
- [x] AC6605 - 已支持

### 功能增强
- [ ] 自动布局算法优化
- [ ] 支持更多 shapes 类型（圆形等）
- [ ] 设备配置模板

## 已知问题
- 暂无

## 示例文件
位于 `examples/` 目录，包含官方示例：
- 1-1RIPv1&v2.topo
- 2-1Single-Area OSPF.topo
- Multi-Area OSPF.topo

## 使用方式
1. 用户描述网络拓扑需求
2. AI 根据 SKILL.md 生成 .topo 文件
3. 用户用 eNSP 打开文件
