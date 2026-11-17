# Fundamentals Self-Check (30-second answers, walk every item)

Every technique the topic uses maps to basics that must come out instantly — examiners judge "did they really build it" by these. Any item you can't answer in 30 seconds is flagged "must fix before the defense".

- **UART**: baud rate / start-stop bits / parity? What does a baud mismatch look like?
- **I2C**: timing (start/stop/ACK)? Why pull-ups, and how sized? Address conflicts?
- **SPI**: four wires and their roles? CPOL/CPHA? Multi-device with CS lines?
- **ADC**: resolution / reference voltage / sample-rate relationship? Quantization error?
- **Interrupts**: why no delay inside an ISR? When is volatile mandatory? How were priorities set?
- **PWM**: how was frequency chosen (motor whine / LED flicker)? Duty cycle vs output?
- **Timer**: prescaler/period math? Input capture vs output compare?
- **FreeRTOS**: inter-task comms (queues / semaphores)? What's priority inversion, how prevented?
- **Motors**: why a flyback diode on the driver? H-bridge in one sentence?
- **Battery power**: how was consumption budgeted? How is low-power mode entered?

**Rule**: answer each item aloud within 30 seconds. Slow-but-correct counts as a warn; wrong counts as a fail.
