*This guide does not apply to the WS2812-SPI driver, which is special. This guide is about SPI-based LEDs which expect a data and a clock line.*

One of the things that the FastLED library will do is attempt to use the fastest mechanism available to it for driving your leds.  This stands out most clearly with SPI based chipsets (e.g. the APA102, WS2801, etc...).

When you set up your leds, you give FastLED a data pin and a clock pin:

```
FastLED.addLeds<APA102,7,11>(leds,NUM_LEDS);
```

You can also adjust the clock speed, eg slowing it down if needed:

```
FastLED.addLeds<APA102,7,11,RGB,DATA_RATE_MHZ(10)>(leds,NUM_LEDS);
```

If the data pin and clock pin that you give FastLED happened to be pins that have hardware SPI available for them, the library will automatically use the hardware SPI system.  Note that under some compiler versions (possibly all, at this point), if you want to set the data rate you have to explicitly specify the clock and data pins.  If, for some reason, you don't want it to use the hardware SPI system, you can force software spi by putting the following at the top of your code:

```
#define FASTLED_FORCE_SOFTWARE_SPI
#include <FastLED.h>
```

Of course, the question then becomes, "What pins are hardware SPI pins?"  Here's a quick rundown:

* Arduino ATMega328P based board:
  * Hardware SPI - data 11, clock 13
  * USART SPI - data 1, clock 4
* Arduino 32U4 based board:
  * Hardware SPI - data 16, clock 15 (on the ISCP header on arduino provided boards)
* Teensy++ 2:
  * Hardware SPI - data 22, clock 21
  * USART SPI - data 3, clock 5
* Teensy 2:
  * Hardware SPI - data 2, clock 1
  * USART SPI - data 8, clock 23
* Arduino ATMega1280/2560 based boards:
  * Hardware SPI - data 51, clock 53 
* Teensy 3/3.1:
  * Hardware SPI - data 11, clock 13
  * Hardware SPI - data 7, clock 14
* Arduino Due:
  * Hardware SPI - data 75, clock 76
* **ESP32 (all variants — ESP32-dev, S2, S3, C3, C6, H2, P4):**
  * **Any GPIO pair works.** ESP32 routes SPI peripherals through the GPIO matrix, so there is no fixed MOSI/SCK pin — whatever pair you pass to `addLeds<APA102, DATA_PIN, CLOCK_PIN>(...)` will be bound to a hardware SPI host at runtime. No `#define` is required to opt in; FastLED will use hardware SPI automatically.
  * If an older build emits the legacy pragma `"No hardware SPI pins defined. All SPI access will default to bitbanged output"`, that message is obsolete — it comes from a platform that predates the ESP32 SPI rework and does not apply to current ESP32 builds. Verified by the FastLED ESP32 SPI driver (`src/platforms/esp/32/drivers/spi/`), which binds any pin pair via `SPI2_HOST` / `SPI3_HOST` and the GPIO matrix.
  * Multi-lane parallel SPI is also available on ESP32 (1-, 2-, 4-, 8-lane) for APA102 / SK9822 / LPD8806 style chipsets — see the ESP32 [ARCHITECTURE.md](https://github.com/FastLED/FastLED/blob/master/src/platforms/esp/32/ARCHITECTURE.md#hardware-spi-vs-clockless-spi) for the driver map.
  * The clock-rate argument works normally: `FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, RGB, DATA_RATE_MHZ(10)>(leds, NUM_LEDS);`.
* ESP8266:
  * Hardware SPI (`HSPI`) — data GPIO13 (MOSI), clock GPIO14 (SCLK). These are fixed; bit-banging is used on any other pair.

### What about USART SPI? ###

You will notice that on Atmega328p based boards the library supports using the USART in SPI mode as well.  You will also notice that this is not available on the other arduino boards.  This is because the arduino folks, in their infinite wisdom, decided to wire the XCK line to an led, rather than anything that you can get at.  So, no USART based SPI for you there.

It is possible that I can use the USARTs on the Teensy 3/3.1 and Arduino Due for SPI as well.  This will come in future revisions of the library if so.

### What about the other SPI/USART pins ###

On most devices, the SPI hardware wants four pins - data in, data out, clock, and a select line.  While writing led data only uses the data out and clock pins, on some platforms using the SPI hardware disables the use of the other pins:

* Teensy 3/3.1: Will disable the use of the MISO pin while writing led data, but will enable it again afterwards. 
* Hardware SPI on AVR based devices: Will disable the use of the MISO and SELECT pins while writing led data, but will enable it again afterwards
* UART in SPI mode on AVR based devices: The RX pin may or may not be available (needs further testing).  Note that if you use the UART in SPI mode for leds, you will not be able to use the UART as a UART for other purposes.  Note that using Serial for printing uses the UART on the Atmega328p.
* Hardware SPI on the arduino DUE: The MISO pin will be unavailable for use

### Getting four hardware SPI lines for the APA102 out of the Teensy 3.0/3.1/3.2 ###

It is possible to get four hardware SPI outputs on the teensy 3.0/3.1/3.2, if you are driving APA102 (note: this hack won't work with most other SPI style led chipsets - though it might with with LPD8806).  You can setup the lines like so:

```
CRGB leds[4][NUM_LEDS];

...

FastLED.addLeds<APA102,7,13>(leds[0],NUM_LEDS);
FastLED.addLeds<APA102,7,14>(leds[1],NUM_LEDS);
FastLED.addLeds<APA102,11,13>(leds[2],NUM_LEDS);
FastLED.addLeds<APA102,11,14>(leds[3],NUM_LEDS);
```

Note that you will have two wires coming off of each of pins 7, 11, 13, and 14.  This (ab)uses the fact that when you're driving led data on pins 7/13 - the clock on pin 13 is strobing, and the data line on pin 7 is pushing out data.  The APA102 strip that is connected to 7/14 won't do anything while that's being written out because its clock line (14) isn't doing anything.  Ditto the strip connect to 11/13, because while it's clock line is going, the data line (11) is staying low, and APA102's data format requires 1's at the beginning of each LED's worth of data to start the frame.  This shuffle then repeats for the other 3 combinations of leds.