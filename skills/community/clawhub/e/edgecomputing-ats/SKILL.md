---
name: "edgecomputing-ats"
description: "Analyzes EdgeComputing ATS (Automatic Ticket System) codebase architecture, device protocols, and business logic. Invoke when user asks about ATS project structure, device management, or needs code analysis."
---

# ATS (Automatic Ticket System) Analyzer

Analyzes the EdgeComputing ATS project for architecture understanding, device management, and codebase navigation.

## ATS Project Overview

ATS is an edge computing gateway for automatic ticket systems, managing multiple hardware devices (IC card readers, QR scanners, LED/LCD displays, card dispensers/collectors, etc.) and communicating with cloud platforms.

### Project Location
```
/home/forlinx/Documents/trae_projects/workspace/EdgeComputing/ats/
```

### Key Documentation
- `docs/系统架构文档.md` - System architecture (layered architecture, modules, communication)
- `docs/项目概述文档.md` - Project overview (features, users, components)
- `docs/用户操作手册.md` - User operation manual
- `docs/设计说明书.md` - Design specification (interfaces, protocols, algorithms)

## Architecture Layers

### Layer 1: Application Layer
- `robot/ats-robot-server/` - Main service (core business logic)
- `robot/ats-robot-lcd-app/` - LCD application (HMI)

### Layer 2: Common Libraries
- `common/ats_common/` - Serial, network, database utilities
- `common/ats_common_device/` - Device abstraction layer (20+ device types)
- `common/ats_media/` - Video capture/encoding
- `common/ats_protocol_api/` - Uplink protocol (cloud communication)
- `common/ats_protocol_robot/` - Downlink protocol (device communication)

### Layer 3: Device Drivers
- `device/io/` - IO devices (GPIO, relay)
- `device/ic/` - IC card readers (multiple vendors: dy, hh, jt, yc, robot)
- `device/qr/` - QR/barcode scanners
- `device/led/` - LED displays
- `device/provide/` - Card dispensers
- `device/collect/` - Card collectors
- `device/plate/` - License plate recognition
- And more (printer, env, aircond, alarm, etc.)

## Core Device Types

| Device Type | Class | Description |
|-------------|-------|-------------|
| IO | CATSIODevice | Digital input/output control |
| IC Card | CATSICDevice | Card read/write (M1, CPU) |
| QR Code | CATSQRDevice | Barcode/QR scanning |
| LED | CATSLEDDevice | Information display |
| LCD | CATSLCDDevice | Human-machine interface |
| Provide | CATSProvideDevice | Card dispensing |
| Collect | CATSCollectDevice | Card collection |
| Plate | CATSPlateDevice | License plate recognition |
| Printer | CATSPrinterDevice | Receipt printing |

## Key Classes

### CNodeService (Main Service)
```cpp
class CNodeService : public CService {
    // Device management
    CATSIODevice*        m_pIODevice;
    CATSProvideDevice*   m_pProvideDevice;
    CATSCollectDevice*   m_pCollectDevice;
    CATSQRDevice*        m_pQRDevice1;
    CATSLEDDevice*       m_pATSLEDDevice;

    // Business management
    CCoilManager*        m_pCoilManager;
    CKioskManager*       m_pKioskManager;

    // Communication
    CMQTTServer*         m_pMQTTServer;
    CDYProtocolServer*   m_pDYProtocolServer;
};
```

### Device Base Class
```cpp
class CATSBaseDevice : public CBaseInterface {
    virtual BOOL Open(...) = 0;
    virtual void Close() = 0;
    void SetStatusHandle(CATSBaseDeviceStatusHandle* pHandle);
};
```

## Communication Architecture

### Cloud Communication (Uplink)
- HTTP Server (Port 8080)
- WebSocket (Port 8081)
- MQTT (Port 1883)
- GB28181 (Port 5060)
- RTSP (Port 554)

### Device Communication (Downlink)
- Serial (RS232/RS485/UART)
- TCP/UDP Network
- CAN Bus
- GPIO

## Message Protocol Examples

### Heartbeat (Uplink)
```cpp
struct ATSCmdHeartonline {
    unsigned int dwDeviceId;
    unsigned char byStatus;
    unsigned char byNetwork;
    unsigned short wDeviceType;
    unsigned int dwOnlineTime;
};
```

### Card Provide Command
```cpp
struct ATSCmdCardProvide {
    unsigned int dwCardType;
    unsigned int dwCardNum;
    unsigned char byAction;  // 1-issue, 2-recycle
};
```

## Compilation

```bash
cd ats/build-aarch64
./build.sh
```

## Usage Guidelines

1. When user asks about ATS architecture, reference the documentation in `docs/`
2. When analyzing device code, look in `device/{type}/` for vendor-specific implementations
3. When analyzing protocol code, look in `common/ats_protocol_*/`
4. Device abstraction is in `common/ats_common_device/`

## Triggers
- User asks about ATS project structure
- User needs help understanding device protocols
- User wants to add new device support
- User asks about system design or architecture
