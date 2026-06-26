---
name: Arduino
description: Develop Arduino projects avoiding common wiring, power, and code pitfalls.
metadata: {"clawdbot":{"emoji":"🔌","os":["linux","darwin","win32"]}}
---

## Voltage and Power Traps
- 3.3V vs 5V logic mixing damages boards — ESP32 is 3.3V, Uno is 5V, level shifter required
- USB provides max 500mA — not enough for motors, servos, or many LEDs
- Never power motors from Arduino 5V pin — use external supply with common ground
- Brown-out causes random resets — looks like code bugs, actually insufficient power
- Decoupling capacitors (0.1µF) near sensor power pins — reduces noise-related glitches

## Wiring Mistakes
- Floating inputs read random values — always use pullup or pulldown resistor
- All components must share common ground — separate grounds = nothing works
- Long wires pick up noise — keep analog sensor wires short
- LEDs need current limiting resistors — direct connection burns LED and pin
- Reversed polarity destroys components — double-check before powering on

## Pin Conflicts
- RX/TX pins (0, 1) conflict with Serial — avoid for GPIO when using Serial Monitor
- Some pins have special functions — check board pinout for I2C, SPI, interrupt-capable pins
- PWM only on pins marked with ~ — `analogWrite()` on wrong pin does nothing
- Internal pullup available — `INPUT_PULLUP` eliminates external resistor for buttons

## Timing Traps
- `delay()` blocks everything — nothing else runs, no input reading, no interrupts serviced
- `millis()` for non-blocking timing — compare against last action time
- `millis()` overflows after ~50 days — use subtraction: `millis() - lastTime >= interval`
- Interrupts for time-critical events — `attachInterrupt()` responds immediately

## Memory Constraints
- Uno has only 2KB RAM — large arrays fail silently with weird behavior
- `F()` macro keeps strings in flash — `Serial.println(F("text"))` saves RAM
- `PROGMEM` for constant arrays — keeps data out of RAM
- String class fragments heap — prefer char arrays for stability

## Serial Debugging
- Baud rate must match — mismatch shows garbage, not an obvious error
- `Serial.begin()` required in setup — output before this goes nowhere
- Serial printing slows execution — remove or reduce for production code

## Upload Problems
- Wrong board selected — uploads but doesn't run correctly
- Serial Monitor holds port — close before uploading
- USB cable might be power-only — some cheap cables don't carry data
- Bootloader corrupted — reflash using another Arduino as ISP

## Sensor Communication
- I2C devices share bus — check for address conflicts with scanner sketch
- 5V sensors on 3.3V boards give wrong readings or damage — check operating voltage
- SPI needs separate CS per device — can't share chip select lines
