A collection of known platform limitations/errata (a work in progress):

* ~~On the Arduino Megas, you can't use pins 6,7,8,9,14,15,16,17,42,43,44,45,46,47,48,49,62,63,64,65,66,67,68,69 with 3-wire chipsets.  This is because the timing for accessing PORT H-L is more expensive than the other ports, and it throws all the timing off.~~ <-- fixed on the FastLED 3.1 branch now
* In order to keep scale8 _fast_ on 8-bit platforms, it is quite literally ((x*s)>>8) (but done in asm) to minimize the cycle count.  This has the side effect of meaning that when the scaling value is set to the max, at 255, it will still scale down the value (e.g. 1 to 0, 255 becomes 254)
* On the teensy 3/3.1 platforms the library allows interrupts while writing out WS2811 leds.  However, the interrupt handling functions still need to be _very fast_, otherwise it will interfere with the writing out of led data, either corrupting your output or cutting your frames off.  If you run into problems like this (N.B. this is reported to happen often with the audio library) either switch to an LED chipset that doesn't care about being interrupted (like the APA102) or put the following line at the top of your .ino file to disable interupts (before any of the #include statements):
```
#define FASTLED_ALLOW_INTERRUPTS 0
```
