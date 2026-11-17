# 8-Category Prior Table (recent cohorts, empirically calibrated)

| # | Category | Typical topics | Difficulty | BOM (USD, single-unit retail) | References | Defense impact | Differentiation | Failure point |
|---|------|--------|------|-----|--------|----------|------------|--------|
| 1 | Classic control / environment sensing | Smart home, environment monitoring, smart lamp, greenhouse, nurse-call | ★★ | $15–30 | ★★★★★ | Medium | Small (must add a new feature) | Plagiarism check & examiner fatigue zone |
| 2 | Smart robot car | Line-following / obstacle-avoidance / Bluetooth RC car | ★★–★★★ | $20–35 | ★★★★★ | Medium | Small | "Top pick + top failure": examiners always ask "how is this different from the kit?" |
| 3 | Wireless networking | LoRa / NB-IoT / WiFi-MQTT smart streetlight, agriculture monitoring, meter reading | ★★★ | $20–40 | ★★★ | Medium-high | Good | NB-IoT modules pricey + SIM subscription fees; shared-accommodation network limits |
| 4 | **AI voice** | ESP32-S3 + offline speech / LLM: voice assistant, companion toy, voice hub | ★★★ | $20–40 | ★★ (growing fast) | **Outstanding** | **Excellent** | Architecture trap: offline recognition vs online LLM pipeline must be decided early |
| 5 | Machine vision | OpenMV / K210 / Raspberry Pi: recognition, tracking gimbal | ★★★★ | $30–60 | ★★★★ | Outstanding | Medium (many people do it) | Debugging has a high floor; takes 2× longer than other tracks |
| 6 | Host-PC + MCU pair | STM32 + Python/Qt/C# dashboard: data acquisition + monitoring platform | ★★★ | $20–35 | ★★★ | High (shows engineering maturity) | Good | Underrated: few students can write a decent host-side app |
| 7 | Motion control | Balance robot, inverted pendulum, gimbal, BLDC | ★★★★ | $30–50 | ★★★ | Good (great story) | Medium | PID tuning time is unpredictable (one night to two weeks) |
| 8 | Signal processing / biomedical | Filter design, high-precision heart-rate capture, smart pill box | ★★★ | $15–35 | ★★★ | Medium | Medium | Medical red line: no diagnostic functionality (regulated medical device territory) |

**Table rule**: for ★★ reference categories, multiply module development time by 1.4 (the hidden cost of having nobody to ask when stuck).

# Cliche Blacklist

smart trash bin, bare line-following/obstacle-avoidance car, temperature-humidity + OLED display, ESP8266 remote light switch, IR smart fan, fingerprint door lock, module-stack digital calendar.

# Fix Formula: Classic Topic + One New Element = Safe Yet Fresh

| Original (blacklisted) | After increment | Increment point |
|---|---|---|
| Line-following car | Car + PID line-following + encoder odometry + OTA firmware update | Jumps from kit-level to an engineering topic with comms protocol + bootloader |
| Digital calendar | Calendar + self-written lunar calendar algorithm (no library) + SD-card logging | Real substance when the examiner asks "how does your lunar algorithm work?" |
| Environment monitoring | Environment monitoring + local smart alerting + FreeRTOS multi-task | Upgrades from "read register → display" to algorithms and scheduling |
| Any topic | + ESP32-S3 offline voice / LLM integration | The strongest defense differentiator in current cohorts, cost comparable to classic topics |

Increment priority: algorithm closed loop > comms & upgrade (OTA) > data outlet (host app / cloud / SD card) > AI interaction.
