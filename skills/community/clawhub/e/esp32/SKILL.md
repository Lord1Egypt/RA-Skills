---
name: ESP32
description: Avoid common ESP32 mistakes — GPIO conflicts, WiFi+ADC2 trap, deep sleep gotchas, and FreeRTOS pitfalls.
metadata: {"clawdbot":{"emoji":"📟","os":["linux","darwin","win32"]}}
---

## GPIO Restrictions
- Strapping pins boot behavior — GPIO0, GPIO2, GPIO12, GPIO15 affect boot mode
- GPIO6-11 connected to flash — don't use, crashes immediately
- GPIO34-39 input only — no output, no pullup/pulldown
- ADC2 unusable with WiFi active — use ADC1 (GPIOs 32-39) when WiFi enabled

## Deep Sleep
- Only RTC GPIOs for wakeup — GPIO0, 2, 4, 12-15, 25-27, 32-39
- `RTC_DATA_ATTR` for persistent variables — regular RAM lost in deep sleep
- `esp_sleep_enable_ext0_wakeup()` for single pin — `ext1` for multiple pins
- WiFi reconnect takes 1-3 seconds after wake — plan for this delay

## WiFi Gotchas
- Call `WiFi.mode()` before `WiFi.begin()` — mode affects behavior
- `WiFi.setAutoReconnect(true)` doesn't always work — implement reconnect in loop
- Event-driven with `WiFi.onEvent()` more reliable — don't poll `WiFi.status()`
- Static IP faster than DHCP — saves 2-5 seconds on connect

## FreeRTOS
- Default stack too small for printf/WiFi — use 4096+ for complex tasks
- Task watchdog triggers at 5s default — call `vTaskDelay()` or feed watchdog
- `xTaskCreatePinnedToCore()` for core affinity — WiFi on core 0, your code on core 1
- `delay()` yields to scheduler — `vTaskDelay(pdMS_TO_TICKS(ms))` in tasks

## Memory
- Heap fragments over time — preallocate buffers, avoid repeated malloc/free
- `ESP.getFreeHeap()` for monitoring — log periodically in long-running apps
- PSRAM available on some boards — `heap_caps_malloc(size, MALLOC_CAP_SPIRAM)`
- String concatenation fragments heap — use `reserve()` or char arrays

## Peripherals
- No native `analogWrite()` — use LEDC: `ledcSetup()`, `ledcAttachPin()`, `ledcWrite()`
- I2C needs external pullups usually — internal pullups too weak for fast speeds
- SPI CS pin must be managed — `SPI.begin()` doesn't auto-configure
- UART0 is Serial/USB — use UART1/2 for external devices

## OTA Updates
- Needs two OTA partitions — default partition scheme may have only one
- Check `ESP.getFreeSketchSpace()` — OTA fails silently if not enough space
- `ArduinoOTA` blocks during update — handle in loop, not in time-critical code

## Power
- Brown-out detector resets at ~2.4V — `esp_brownout_disable()` if using battery
- WiFi TX uses 300mA peaks — power supply must handle spikes
- Deep sleep ~10µA — but RTC peripherals add more if enabled
