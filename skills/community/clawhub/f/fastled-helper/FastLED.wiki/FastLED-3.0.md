# FastLED ~~2.1~~ 3.0

We're proud to announce a fabulous new version of FastLED, an open source LED animation library for Arduino.  This new version supports lots of new hardware and also includes:
* vibrant new color, light, and power controls,
* more than ten new example animations for you to remix (including 'fire'),
* high performance math functions including fast sine and cosine, and
* absolutely the fastest Perlin/Simplex noise generators ever seen on Arduino.

A big thanks goes out to the entire FastLED community, who've helped shape and refine this library, and who have built some absolutely stunning projects with it.

Here's some more detail on what's in this release:

New Microcontroller Support Added
* Arduino Due
* Teensy 3.1
* Digistump DigiX
* Continued support for most other Arduino boards (Uno, Leonardo, Nano, Micro, etc.), the Adafruit Trinket, Gemma, and Flora, as well as PJRC Teensy 2 and Teensy 3.0.

New LED Chip Support Added
* APA102
* APA104
* GW6205 / GW6205_400
* LPD1886
* P9813 Total Control Lighting LEDs
* USC1903_400
* SmartMatrix
* Continued support for NeoPixel, WS2811, WS2812, WS2812B, WS2801, LPD8806, TM1809, TM1804, TM1803, and SM16716!

New Color, Light, and Power Controls
* Programmable Color Palettes (CLUTs)
* High-speed temporal dithering for smooth dimming with the master brightness control
* Ability to calibrate each strip's RGB colors
* Ability to adjust the LED white point / temperature
* Ability to automatically limit LED power draw (current)

Perlin/Simplex Noise
* 1- 2- and 3-dimensional Perlin/Simplex noise
* Multiple octave noise support
* Example sketches using 'noise' for animated texture generation

New Example Sketches
* XYMatrix - show how to use a 2-D matrix of leds
* Fire2012 - simple, fast fire simulation
* Perlin/Simplex Noise - dynamic texture animation examples
* ColorPalette - showing how to use color palettes (CLUTs)
* ColorTemperature - color correction and white point adjustment
* Examples showing how to drive multiple independent LED strips

High Performance Math Package
* High-speed sine and cosine
* Cubic, triangle, and quadratic wave functions
* In/Out easing functions

And Also...
* Many bug fixes and performance improvements, and 
* A big, shiny new version number to go with all this great code


Daniel Garcia & Mark Kriegsman, October 2014
