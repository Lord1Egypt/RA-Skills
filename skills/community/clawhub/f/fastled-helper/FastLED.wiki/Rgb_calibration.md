# Introduction

With the FastLED library, under examples, there is a sample program called RGBCalibrate.  Use this to set the RGB ordering for the LED pixels that you have, as some manufacturers change up the wiring and RGB ordering.

# Details

Use this sketch to determine what the RGB ordering for your chipset should be.  Steps for setting up to use:

 * Uncomment the line in setup that corresponds to the LED chipset that you are using.  (Note that they all explicitly specify the RGB order as RGB)
 * Define DATA_PIN to the pin that data is connected to.
 * (Optional) if using software SPI for chipsets that are SPI based, define CLOCK_PIN to the clock pin
 * Compile/upload/run the sketch 

You should see six leds on.  If the RGB ordering is correct, you should see 1 red led, 2 green 
leds, and 3 blue leds.  If you see different colors, the count of each color tells you what the 
position for that color in the rgb orering should be.  So, for example, if you see 1 Blue, and 2
Red, and 3 Green leds then the rgb ordering should be BRG (Blue, Red, Green).  

You can then test this ordering by setting the RGB ordering in the addLeds line below to the new ordering
and it should come out correctly, 1 red, 2 green, and 3 blue.

# Now what?

Now that you have the ordering, you can use it in your addLeds line to set the rgb ordering for your pixels, for example:

```
void setup() { 
  LEDS.addLeds<WS2811,DATA_PIN, GRB>(leds, NUM_LEDS);
}
```
