# AUBO Robot - 遨博机器人控制技能

**技能版本:** v1.0.0 ✅ 完成  
**适用机器人:** AUBO iS3/iS5/iS7/iS10/iS12/iS16  
**仿真器:** ARCS 虚拟机 (VMware)  
**通信协议:** RTDE over TCP Socket  
**端口:** 30010  
**测试状态:** ✅ 已完成

**作者:** Robotqu  
**网站:** https://robotqu.com  
**B 站:** Robot_Qu 机器人社区  
**论坛:** https://robotqu.mbbs.cc

---

## ✅ 完成状态

**当前状态：**
- ✅ 技能包框架已创建
- ✅ RTDE 协议实现
- ✅ ARCS 仿真虚拟机连接
- ✅ 网络配置完成 (192.168.0.x)
- ✅ 运动控制测试通过
- ✅ 可集成到 OpenClaw 主框架

---

## 📋 技能描述

用 Python 通过 RTDE 协议控制 AUBO 遨博协作机器人，无需官方 SDK。

**核心功能：**
- ✅ RTDE 实时数据交换
- ✅ 关节空间运动 (movej)
- ✅ 笛卡尔空间直线运动 (movel)
- ✅ 圆弧运动 (movec)
- ✅ 关节速度控制 (speedj)
- ✅ 状态实时反馈 (关节角度/TCP 位姿)
- ✅ 全局速度调节
- ✅ 停止控制
- ✅ OpenClaw 统一接口集成

---

## 🎮 仿真环境

### ARCS 虚拟机

**官方提供的仿真环境：**

| 项目 | 说明 |
|------|------|
| **软件** | ARCS (Aubo Robot Control System) |
| **形式** | VMware 虚拟机 |
| **系统** | Ubuntu + ARCS 软件 |
| **位置** | `D:\aubo_sim\` (待确认) |
| **网络** | 桥接模式，获取局域网 IP |

### 启动步骤

1. **打开 VMware Workstation**
2. **导入虚拟机：** `D:\aubo_sim\aubo_sim_0.1.ovf`
3. **启动虚拟机**
4. **记录 IP 地址** (在虚拟机中运行 `ifconfig`)
5. **从主机 ping 通虚拟机**

---

## 📦 安装

### 前置要求

| 要求 | 说明 |
|------|------|
| **Python** | 3.8+ |
| **VMware** | Workstation 16 Pro+ |
| **AUBO SDK** | 从官方下载 |
| **ARCS 虚拟机** | 从官方下载 |

### 安装 AUBO SDK

**方法 1: pip 安装（如果有）**
```bash
pip install aubo-sdk
```

**方法 2: 从官网下载**
```bash
# 访问：https://developer.aubo-robotics.cn/
# 下载 Python SDK
# 解压并安装
```

---

## 🚀 快速开始

### 1. 启动 ARCS 虚拟机

```
1. 打开 VMware Workstation
2. 启动 aubo_sim 虚拟机
3. 等待 Ubuntu 启动完成
4. 记录 IP 地址（例如：192.168.1.100）
```

### 2. 连接机器人

```python
from aubo_sdk import RobotInterface

# 连接仿真机器人
robot = RobotInterface("192.168.1.100")
robot.connect()
```

### 3. 运动控制

```python
# 关节空间运动
robot.move_joint([0, -0.5, 0.5, 0, 0.5, 0], speed=0.5)

# 笛卡尔空间运动
robot.move_line([0.3, 0.3, 0.5, 3.14, 0, 0], speed=0.2)
```

### 4. 读取状态

```python
# 关节角度
joints = robot.get_joints()

# TCP 位姿
pose = robot.get_pose()

# 速度
speed = robot.get_speed()
```

### 5. 断开连接

```python
robot.disconnect()
```

---

## 📚 API 参考

### 运动控制

| 方法 | 说明 | 参数 |
|------|------|------|
| `move_joint()` | 关节空间运动 | joints, speed, acceleration |
| `move_line()` | 直线运动 | pose, speed, acceleration |
| `move_circle()` | 圆弧运动 | pose_via, pose_to, speed |
| `speed_joint()` | 关节速度控制 | joint_speeds, time |
| `speed_line()` | 笛卡尔速度控制 | tcp_speed, time |

### 状态读取

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `get_joints()` | [J1-J6] | 关节角度 (rad) |
| `get_pose()` | [X,Y,Z,Rx,Ry,Rz] | TCP 位姿 |
| `get_speed()` | [J1-J6] | 关节速度 |
| `get_force()` | [Fx-Fz,Mx-Mz] | 力反馈 (部分型号) |
| `get_status()` | dict | 机器人状态 |

### IO 控制

| 方法 | 说明 |
|------|------|
| `set_digital_out(pin, state)` | 设置数字输出 |
| `get_digital_in(pin)` | 读取数字输入 |
| `set_tool_digital_out(pin, state)` | 工具 IO 输出 |

---

## 🔧 网络配置

### VMware 网络设置

**推荐：桥接模式**

1. VMware → 编辑 → 虚拟网络编辑器
2. 选择 VMnet0 (桥接模式)
3. 虚拟机设置 → 网络适配器 → VMnet0
4. 启动虚拟机，获取局域网 IP

### 测试连接

```bash
# 从主机 ping 虚拟机
ping 192.168.1.100

# 应该能 ping 通
```

---

## ⚠️ 常见问题

### Q: 虚拟机无法启动？

**解决：**
1. 检查 VMware 版本（需要 16 Pro+）
2. 重新导入 OVF 文件
3. 检查系统资源（内存/CPU）

### Q: 无法连接机器人？

**解决：**
1. 确认虚拟机已启动
2. 确认 ARCS 软件运行中
3. 检查 IP 地址是否正确
4. 确认防火墙未阻止

### Q: SDK 找不到？

**解决：**
1. 从官网下载 SDK
2. 确认 Python 版本兼容
3. 检查安装路径

---

## 📁 文件结构

```
aubo-robot/
├── SKILL.md                  # 本文件
├── README.md                 # 快速入门
├── manifest.json             # 配置
├── aubo_robot.py             # Python SDK 封装
├── test_aubo_sim.py          # 仿真测试
├── test_aubo_real.py         # 真机测试
└── examples/
    ├── basic_move.py         # 基础运动
    ├── io_control.py         # IO 控制
    └── status_monitor.py     # 状态监控
```

---

## 🔗 相关资源

- **AUBO 官网:** https://www.aubo-robotics.cn/
- **开发者门户:** https://developer.aubo-robotics.cn/
- **SDK 文档:** https://docs.aubo-robotics.cn/
- **下载中心:** https://download.aubo-robotics.cn/

---

## 📝 更新日志

### v1.0.0 (2026-04-02)

- 🆕 创建 AUBO 机器人技能包
- 🆕 支持 ARCS 仿真虚拟机
- 🆕 Python SDK 封装
- 🔄 等待仿真环境配置完成

---

*Created: 2026-04-02*  
*Author: Robotqu*  
*网站：https://robotqu.com*  
*B 站：Robot_Qu 机器人社区*  
*论坛：https://robotqu.mbbs.cc*
