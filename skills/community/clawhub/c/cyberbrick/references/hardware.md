# Cyberbrick Hardware Components

This document provides an overview of the electronic and mechanical components available in the Cyberbrick ecosystem.
*Source: Extracted from https://wiki.bambulab.com/en/cyberbrick/components/component-list on 2026-02-23.*

---

## I. Core & Control Boards

### 1. Multi-Function Core Board (XA003)
- **Description**: The central processing unit of any Cyberbrick project. Based on the ESP32-C3 MCU, it provides logic control, wireless connectivity (Bluetooth & WiFi), and programming capabilities via MicroPython.
- **Key Features**:
    - **CPU**: ESP32-C3
    - **Connectivity**: Bluetooth, WiFi
    - **Ports**: USB-C for programming and power.
    - **Input Voltage**: 5V (USB-C), 3.7V–12.6V (Battery)
    - **Programmable**: Supports Cyber-Script (block-based) and MicroPython.

### 2. Remote Control Transmitter Shield (XA005)
- **Description**: An expansion board for the Core Board that turns it into a remote control transmitter. It provides interfaces for input devices.
- **Key Features**:
    - **Input Channels**: 6x Analog (joysticks, switches), 4x Digital (buttons).
    - **Connectors**: 3-pin SH1.0 for analog, 2-pin SH1.0 for digital.
    - **Power**: 2-pin XH2.54 connector (4.5V–12.6V).

### 3. Remote Control Receiver Shield (XA004)
- **Description**: An expansion board for the Core Board that allows it to receive signals and control output devices.
- **Key Features**:
    - **Output Channels**: 2x DC Motor ports, 4x Servo ports, 2x LED ports.
    - **Connectors**: 2-pin SH1.0 (Motors), 3-pin headers (Servos), 3-pin SH1.0 (LEDs).
    - **Power**: 2-pin XH2.54 connector (7.4V–12.6V).
    - **Max Current**: 3A.

---

## II. Input Modules (Sensors & Controls)

- **Single-Axis Joystick (XA009)**: Single-channel analog input, auto-centering. Ideal for speed or position control.
- **Dual-Axis Joystick (XA011)**: Two-channel analog input, auto-centering. For controlling both speed and direction.
- **Three-Position Rocker Switch (XA010)**: Single-channel analog input with three fixed states.
- **Momentary Button (XA008)**: Digital input module recognizing short press, long press, etc.
- **Power Switch Module (XA007)**: A simple switch to control power flow from the battery.

---

## III. Output Modules (Motors, Servos, Lights)

### Motors & Servos
- **030 Micro DC Motor (LA024)**: A compact brushed motor for continuous motion.
- **N20 Reduction Gear Motor**: Smaller brushed motors available in various speeds (150, 400, 1000 RPM).
- **9g Positional Digital Servo (180° - PG001)**: A servo that maintains a specific angle. Ideal for steering.
- **9g Continuous Rotation Digital Servo (360° - PG002)**: A servo that provides continuous rotation at a controlled speed.

### Lighting
- **WS2812 RGB LED (KB003)**: An individually addressable RGBW LED board.
- **WS2812 LED Hub (XA006)**: Connects and controls multiple WS2812 LED boards from a single port on the receiver shield.

---

## IV. Power & Wiring

- **14500 7.4V 800mAh Li-ion Battery (PC003)**: The standard rechargeable battery pack.
- **3x1.5V AAA Battery Case**: An alternative power source.
- **Connectors & Wires**: A variety of pre-crimped wires with SH1.0 (2/3-pin) and XH2.54 (2-pin) connectors.

---

## V. Mechanical & Miscellaneous Parts

- **Plastic Differential Gear Kit (LA026)**
- **Rubber Tires (LA027)**
- **Magnets & Springs**
- **Screws & Fasteners**
