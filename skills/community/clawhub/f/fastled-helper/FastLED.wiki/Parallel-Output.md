# Parallel Output on WS2811 style leds

WS2812 strips are slow for writing data, with a data rate of just 800khz, it takes 30µs to write out a single led's worth of data.  One way to improve the performance here is with parallel output, driving 8 lines in parallel gets you, effectively, 8 times the data rate.  One of the first libraries to do this for WS2811 leds (if not the first) is the [OctoWS2811 library for the Teensy 3/3.1](http://www.pjrc.com/teensy/td_libs_OctoWS2811.html).  This library is especially optimized for taking data from USB and shoving it out to the leds, effectively using the Teensy 3.x as a dumb frame buffer.

OctoWS2811 has two limitations for the average FastLED user, however.  The first is that OctoWS2811 uses its own functions for setting color data, and doesn't provide any of the brightness, color correction, math functions, etc... that FastLED does.  In addition, while you could mix libraries and use FastLED to prep your color data then call into OctoWS2811's setpixel functions, for a 64x8 array of leds this would end up taking nearly 2ms worth of calls to setPixel - which is nearly the amount of time it takes to write 512 leds worth of WS2811 data, removing much of the benefit of OctoWS2811.  The second limitation to OctoWS2811 is that it is limited to 8 lines, and a specific set of pins, and the Teensy 3.

## Multi-platform Parallel output

If you are using a due or a digix or a teensy 3 or a teensy 3.1, FastLED now has some new parallel output controllers that will allow you to drive 8 lines of WS2812 strips in parallel.  This means that instead of taking 15.3ms/frame of CPU time to write out 512 bytes of data, it would take closer to 1.9ms/frame. See examples/Multiple/ParallelOutputDemo to see how this works.  

On the teensy 3 and 3.1 there's two sets of pins that we can use for parallel output, described below:

* WS2811_PORTD - the OctoWS2811 pins - 2,14,7,8,6,20,21,5
* WS2811_PORTC - pins 15,22,23,9,10,13,11,12,28,27,29,30 (yes, 12 pins!  If you're willing to solder onto pads on the back of the teensy)
* WS2811_PORTDC - pins 2,14,7,8,6,20,21,5,15,22,23,9,10,13,11,12 <-- 16 pins, no soldering onto pads on the back!

On the due/digix (note: some pins aren't available on the due, which means anything you write to that block of led data will just disappear):

* WS2811_PORTA - pins 69, 68, 61,60,59, 100, 58, 31 (pin 100 only available on the digix)
* WS2811_PORTC - pins 90, 91, 92, 93, 94, 95, 96, 97 (only available on the digix)
* WS2811_PORTD - pins 25,26,27,28,14,15,29,11 (all available on the due)

And on the ESP8266:

* WS2811_PORTA - pins 12, 13, 14 and 15 (or pins 6,7,5 and 8 on the NodeMCU boards/pin layout).

You can also replace WS2811 with WS2811_400, TM1803, and UCS1903 in the above.

## Parallel output on the Teensy 4

The new Teensy 4 also supports parallel output, but it's done slightly differently from the above platforms.  First off, there are three sets of possible pins that can be used - each of the three set of pins, in order:

* First: 1,0,24,25,19,18,14,15,17,16,22,23,20,21,26,27
* Second: 10,12,11,13,6,9,32,8,7
* Third: 37, 36, 35, 34, 39, 38, 28, 31, 30

Note that any pin above 21 is a pad on the back of the board.  This is the ordering of pins for each grouping.  Now, when calling add LEDs, you can pick which pin you want to start with in each group, and how many lanes.  For example, if you want 16 way output, you would use Pin 1 (and the rest of the pins in that first group) (with 4 of the strips having to connect to the backside of the panel).  If you only want a few channels of output, say 6 - and you don't want to use pads on the back, then you can select pin 19 as your initial pin (from that first group), and set the number of channels to 6 which will use pins 19,18,14,15,17,16.  

Again, for the Teensy 4 - you select the first pin that you want for output, and then the number of pins after that in the list from above.  

Then in code, you use addLeds like this:

```
#define NUM_LEDS_PER_STRIP 60
#define NUM_STRIPS 6

CRGB leds[NUM_LEDS_PER_STRIP * NUM_STRIPS];

void setup() {
    FastLED.addLeds<NUM_STRIPS, WS2812, 19, GRB>(leds, NUM_LEDS_PER_STRIP);
}
```

and you have parallel output!  Also note that on the Teensy4 - you specify which clockless chipset you want to use (no more being limited to which chipsets I've defined CHIPSET_PORTX for...) - if this mechanism seems to continue to work well, I may make it available on the other platforms as well, but for now I didn't want to make changes outside of the teensy4.

## Making OctoWS2811 faster with FastLED

If you only have 8 lines of leds, and you are using a Teensy 3/3.1, there's a lot of benefit to using OctoWS2811.  Wanting to encourage people to get the most benefit of what is available to them, FastLED 3.1 introduces an OctoWS2811 controller.  This code preps OctoWS2811's drawing buffer far faster than using setPixel, and gives you the benefit of FastLED's scaling/dithering/color correction code.  How much faster?  For a 64x8 led setup, 500µs vs. 2ms.  You can see this in action in examples/Multiple/OctoWS2811Demo

A comparison of CPU timings, for writing out 512 leds:

* 512 leds on 8 pins, w/FastLED3.0: 15,360µs or 66fps max
* 512 leds on 8 pins, w/OctoWS2811 using setPixel: 2000µs or 500fps max
* 512 leds on 8 pins, w/FastLED3.1 parallel output: 1900µs or 526fps max
* 512 leds on 8 pins, w/FastLED3.1 feeding OctoWS2811: 500µs or 2000fps max (sadly, WS2811's get unhappy if you go above 400-500fps)