---
name: Ai-Thinker-Coder
description: 安信可科技物联网模组开发助手 - 覆盖 WiFi、BLE、LoRa、Radar、NB-IoT、星闪等全系列模组的编程指南。子 skill 按芯片型号分组：BL602(Ai-WB2)、BL616/BL618(Ai-M61/M62) 等。使用 /skill Ai-Thinker-Coder-<chip> 加载特定芯片开发指南。
category: hardware
tags:
  - 安信可
  - Ai-Thinker
  - 物联网
  - IoT
  - 无线模组
  - WiFi
  - BLE
  - LoRa
  - Radar
  - NB-IoT
  - 星闪
  - NearLink
version: 1.0.0
author: 安信可科技 & Hermes Agent
license: MIT-0
metadata:
  hermes:
    tags: [WiFi, BLE, LoRa, Radar, NB-IoT, 物联网, IoT, 模组开发]
    related_skills: [Ai-Thinker-Coder-bl602, Ai-Thinker-Coder-bl618, Ai-Thinker-Coder-lora, Ai-Thinker-Coder-radar]
---

# 安信可科技 (Ai-Thinker) 物联网模组开发指南

安信可科技是专业的物联网无线连接模组厂商，产品涵盖 WiFi、BLE、LoRa、Radar、NB-IoT、星闪等多个系列。

**官网**: https://www.ai-thinker.com  
**技术支持论坛**: https://bbs.ai-thinker.com  
**文档中心**: https://docs.ai-thinker.com

---

## 产品线总览

| 产品系列 | 芯片平台 | 典型模组 | 协议 | 开发环境 |
|---------|---------|---------|------|---------|
| **Ai-WB2** | BL602 | Ai-WB2-01S/12F/32S | Wi-Fi 4 + BLE 5.0 | Linux/Windows |
| **Ai-M61** | BL616/BL618 | Ai-M61-32S/32SU | Wi-Fi 6 + BLE 5.3 + Thread | Linux/Windows |
| **Ai-M62** | BL616/BL618 | Ai-M62-12F/18F | Wi-Fi 6 + BLE 5.3 + Thread | Linux/Windows |
| **BW/RTL87xx** | RTL8720/RTL8721 | BW-LP14 | 双频WiFi + BLE 5.0 | Linux |
| **TG** | - | TG-01L | Wi-Fi (天猫精灵) | AT指令 |
| **LoRa** | - | Ra-01/RA-01H | LoRa/LoRaWAN | Arduino |
| **Radar** | - | RD-01/03/04/6x | 10GHz/24GHz/60GHz | Arduino |

---

## 子 Skill 列表 (按芯片平台)

加载特定芯片平台的开发指南：

```bash
/skill Ai-Thinker-Coder-bl602    # Ai-WB2 系列 (BL602)
/skill Ai-Thinker-Coder-bl618    # Ai-M61/M62 系列 (BL616/BL618) - 待发布
/skill Ai-Thinker-Coder-lora     # LoRa 系列 - 待发布
/skill Ai-Thinker-Coder-radar    # Radar 系列 - 待发布
```

---

## 开发环境快速搭建

### 通用工具

| 工具 | 用途 | 下载 |
|-----|------|-----|
| VSCode | 代码编辑器 | https://code.visualstudio.com/ |
| Git | 版本控制 | https://git-scm.com/ |
| Python 3.8+ | 构建工具 | https://www.python.org/ |

### 串口驱动

| 芯片平台 | 驱动 | 说明 |
|---------|------|-----|
| CH340/CH341 | 点击下载 | USB转串口芯片驱动 |
| CP2102 | 系统自带 | 通常免驱 |

### WSL 开发环境 (推荐)

```powershell
# 安装 WSL2
wsl --install

# 重启后安装 Ubuntu
# 参考: /home/seahi/workspase/vitpress_docs_resoure/docs/zh/development/devel_env_setup/install_wsl.md
```

### USB 转串口映射 (WSL2)

```powershell
# 在 PowerShell (管理员) 中列出 USB 设备
usbipd list

# 绑定设备
usbipd bind --busid <busid>

# 附加到 WSL
usbipd attach --wsl --busid <busid>

# 在 WSL 中验证
ls /dev/ttyACM*
```

---

## 常用链接

- **样品申请**: https://wj.qq.com/s2/18130629/6b69/
- **爱星物联云平台**: https://open.ai-things.com/
- **GitHub SDK**: https://github.com/Ai-Thinker-Open/
- **安信可论坛**: https://bbs.ai-thinker.com/

---

## 使用说明

本 skill 是安信可模组开发的入口指南。使用 `/skill Ai-Thinker-Coder-<芯片平台>` 加载对应芯片的详细开发文档。

### 安装子 Skill

加载主 skill 后，系统会自动提示可用的子 skill。安装子 skill 可以：

**方式一：通过命令安装**
```bash
# 安装 BL602 子 skill
/skill install Ai-Thinker-Coder-bl602
```

**方式二：通过 hermes 命令安装**
```bash
hermes skills install Ai-Thinker-Coder-bl602
```

### 快速开始

1. 安装主 skill：`/skill install Ai-Thinker-Coder`
2. 安装目标芯片的子 skill：如 `/skill install Ai-Thinker-Coder-bl602`
3. 加载子 skill：`/skill Ai-Thinker-Coder-bl602`

详细安装和使用说明请参考:
- [README.md](README.md) - 英文安装指南
- [README_Zh.md](README_Zh.md) - 中文安装指南

---

## 许可证

本项目采用 MIT-0 许可证，详见 [LICENSE](LICENSE) 文件。
