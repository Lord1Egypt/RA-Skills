Here's a list of the chipsets that are currently supported by the library as well as some notes about them based on our experiences.  Information pulled from either data sheets or experimentation.

### Current, supported hotness

* APA102 - (adafruit sells these as dotstars) Fast data rate (I've pushed as fast as 24Mhz), stupid high refresh rate.  I'd recommend these over just about anything else at this point.
* SK9822 - APA102 clone 
* ws2811/ws2812/ws2812B - (adafruit sells these as "neopixels") super cheap (30 leds/m for $6, 60 leds/m for $11!), very slow data rate (800Kbps - meaning you'd want to investigate parallel output for more than a few hundred leds - see paul's excellent OctoWS2811 if you're using a teensy 3 - and i'm currently working on code for FastLED that will allow grouping/blocking of multiple streams of output in parallel - hopefully that will be out some time this year - I had an installation going in on july 4th that used it :).  Also - many of the strips are 1 led, 1 controller, so you can cut at every led.  Even better, is the ws2812 variant, which is the led and chip in a single package (some people still sell these as ws2811 - but the protocol is the same) - so it can be very very compact.  Unfortunately, their data protocol requires disabling interrupts on the avr while writing data out, and so using these leds will interfere with things like IR libraries or using i2c and serial.  **NOTE:** at some point, the timings for WS2811 chips changed to be closer in line to the WS2812 timings.  If you have chips identified as WS2811 that are behaving badly, try changing the chipset reference in addLEds to WS2812, and see if that fixes the issues.
* lpd8806's - less cheap (closer to $16/meter shipped for 48/m), but super fast (i've pushed them at upwards of 22Mbps!).  Also, they're paired, so it's one controller per 2 rgb pixels.  Note that these only really display 7 bits per channel, not 8, so they can really only display 128 different levels of light for each color channel.  Programming API is still 8 bits, but the low bit is meaningless.
* P9813 - This is the chipset used in Cool Neon's Total Control Lighting.  

### Older, still supported, lukewarm

* ws2801 - older, cheap(ish) - but slow (1Mbps), i've found it prone to glitching at longer lengths, and higher data rates are right out.  
* tm1809/1804/1812 - similar in protocol to the ws8211, similar cost benefit when it was out, 1 IC per 3 rgb leds, seems to be a lot twiticher re: line interference (the 1809 controls 3 rgb pixels, the 1804 controls 1)
* tm1803 - slower speed version of the tm1809, sold primarily by radio shack 

### Other stuff

* UCS1903 - similar to tm1809/ws2811.  Not sure why this exists, honestly.  Very very slow protocol, closer to 400kbps.
* UCS1904/2903 - closer in timing to the ws2811.  Some folks find it interesting
* SM16716 - implemented because a couple people asked for it.  Terrible protocol.
* GW6205 - someone asked for these, I haven't ever seen them in person!
* LPD1886 - a 3 wire chipset that is 12-bits per pixel instead of the usually 7/8-bit per pixel most of the other chipsets seen are so far
* DMX controllers (DMXSIMPLE or DMXSERIAL) - if your'e controlling your leds using DMX from an arduino, this will drive DMX using the rest of the led library - note that you will need to ```#include <DmxSimple.h>``` or ```#include <DmxSerial.h>``` _before_ ```#include <FastLED.h>``` to use DMX output.
* Adafruit Pixie leds (PIXIE) - http://www.adafruit.com/product/2741 - in order to use these leds you ```#include <SoftwareSerial.h>``` _before_ ```#include <FastLED.h>```.

### Upcoming

(as in, soon, depending, timeframe), unclear on hotness, or if they will be made to work.

* TM1829 - similar to the TM1809/WS2811, but also allows setting 32 base current levels for brightness/power usage control - i have a set of these, but the code for them doesn't work yet
* TLS3001 - I get a lot of requests for this one.  Unsure what benefits it provides, but among other things it's 12-bits per color vs. 8-bit for most of the currently supported chipsets.
* TI TLC5940 - this is a heavy hitter - also 12 bit color, led color correction support, 16 led channels per chip - i've heard of people doing RGBW with setups like this.﻿
* TI TLC5947 like above, but with 24 channels

Here's a chart listing the various chipsets and pieces of data that we know about them at the moment.  Chipset power draw is how much power a single chip draws when the leds are off, but power is connected:

| Chipset | Supported | Wires | Color Bits | Data Rate | PWM Rate | Chipset Power Draw 
|---------|-----------|-------|------------|---------------|----------|--------------------
| APA102/DOTSTAR | √ | 4 | 8 | ~24Mbps | 20khz | 0.9ma@5v 
| WS2811 | √ | 3 | 8 | 800kbps | 400Hz | 5mw / 1ma@5v 
| WS2812B/NEOPIXEL | √ | 3 | 8 | 800kbps | 400Hz | 5mw / 1ma@5v 
| TM1809/TM1812 | √ | 3 | 8 | 800kbps | 400Hz | 7.2mw / 0.6ma@12v 
| TM1803 | √ | 3 | 8 | 400kbps | 400Hz | 7.2mw / 0.6ma@12v 
| TM1804 | √ | 3 | 8 | 800kbps | 400Hz | 7.2mw / 0.6ma@12v 
| WS2801 | √ | 4 | 8 | 1Mbps | 2.5kHz | 60mw / 5ma@12v 
| UCS1903 | √ | 3 | 8 | 400kbps | unknown | ? 
| UCS2903 | √ | 3 | 8 | 800kbps | unknown | ? 
| LPD8806 | √ | 4 | 7 | 1-20Mbps | 4kHz | ? 
| P9813 | √ | 4 | 8 | 1-15Mbps | 4.5kHz | ? 
| SM16716 | √ | 4 | 8 | ? | ? | ? 
| TM1829 | X | 3 | 8 |  1.6Mbps/800kbps | 7kHz | 6ma@12v 
| TLS3001 | X | ? | 12 | ? | ? | ? 
| TLC5940 | X | 4 | 12 | ? | ? | ? 
| TLC5947 | X | 4 | 12 | ? | ? | ? 
| LPD1886 | X | 3 | 12 | ? | ? | ? 