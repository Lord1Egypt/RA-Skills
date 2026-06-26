Using Multiple Controllers
==========================

One question that we often get is how to use multiple output strips at once with the library.  There's a variety of reasons why someone might want to have multiple strips coming off of their arduino (or other controller):

* Flexibility - perhaps you have an led design where strips are fanning out like the arms of a starfish, your wiring would be much simpler if you could have one controller in the middle driving all the LEDs
* Variety - what if you have 4 strips, all with different types of LED chipsets on them that you want to use together for a project?
* Performance - (NOT YET, but coming) - if you could write out 8 strips in parallel, as fast as it would take you to write 1 strip, it stands to reason that you'd be able to drive 8 times as many leds before, or, conversely, run your current leds 8 times faster!

One of the things to think about is how you'd like to arrange your led data:

* Same led data going to all your strips - so when you write to the first led in your led data, the first led on all your strips has that color, and so on down the line.  Good for setups where you want strips mirroring each other.
* Separate sets of led data going to your strips - you set up separate arrays of CRGB data, one for each led strip.
* An array of led arrays - a sort of in between option that gives you one data structure still, but also somewhat separated data as well.
* Offsetting into one giant led array - you set up one CRGB array for all of your leds, then each strip points to a different segment of that giant array.

We'll talk about these more below, note there will be examples in the library as well that will be referenced that you can use for following along or as a starting point.  Note that all the examples will use the NEOPIXEL led type (as that appears to be fairly common these days, anyway).

Mirroring strips
----------------

Mirroring strips is prettty straight forward.  All you do is tell FastLED what strips you have, and on what pins.  An example of this is shown in the library's Examples folder, under Multiple/MirroringSample.  In this sample, we have 4 strips of NeoPixel leds, on pins 4, 5, 6 and 7.  Each strip has 60 leds on it.

The first thing that we'll do in our code is set up our led data:

```C++
#include "FastLED.h"
#define NUM_LEDS_PER_STRIP 60
CRGB leds[NUM_LEDS_PER_STRIP];
```

This is going to be the array of our led data.  

Next, we need to actually tell FastLED what led strips we have, and on what pins:

```C++
void setup() {
  FastLED.addLeds<NEOPIXEL, 4>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 5>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 7>(leds, NUM_LEDS_PER_STRIP);
}
```

Each call to FastLED.addLeds tells the library about your leds.  In the code above, we're telling the library "There's four neopixel strips, on pins 4, 5, 6, and 7.  Each strip is using our led array leds, and has NUM_LEDS_PER_STRIP (which we've defined to be 60)."

Now, there's nothing special to do in the rest of your code.  If you want a simple moving dot, you can just do:

```C++
void loop() {
  for(int i = 0; i < NUM_LEDS_PER_STRIP; i++) {
    leds[i] = CRGB::Red;    // set our current dot to red
    FastLED.show();
    leds[i] = CRGB::Black;  // set our current dot to black before we continue
  }
}
```

Now, when this code is run, each strip will have a dot moving back and forth along it, all four in perfect sync/harmony with each other!


Multiple led arrays
-------------------

Of course, sometimes you may want your different strips to do different things.  For this example, there's say there's three led strips, on pins 10, 11 and 12.  You want a moving dot again, but this time, you want the first strip to have a red dot, the second strip to have a green dot, and the third strip to have a blue dot.  This time, instead of one CRGB array named leds, we're going to make three, helpfully named for what we're doing (this example is in Examples, under Multiple/MultiArrays):

```C++
#include "FastLED.h"
#define NUM_LEDS_PER_STRIP 60
CRGB redLeds[NUM_LEDS_PER_STRIP];
CRGB greenLeds[NUM_LEDS_PER_STRIP];
CRGB blueLeds[NUM_LEDS_PER_STRIP];
```

Our setup function looks a little bit like the one above did, however this time we're pointing each strip at a different led array:

```C++
void setup() {
  FastLED.addLeds<NEOPIXEL, 10>(redLeds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 11>(greenLeds, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 12>(blueLeds, NUM_LEDS_PER_STRIP);

}
```

Now, this time, since we have three sets of led data, in our loop function we're going to need to write what we want into each array separately:

```C++
void loop() {
  for(int i = 0; i < NUM_LEDS_PER_STRIP; i++) {
    // set our current dot to red, green, and blue
    redLeds[i] = CRGB::Red;
    greenLeds[i] = CRGB::Green;
    blueLeds[i] = CRGB::Blue;
    FastLED.show();
    // clear our current dot before we move on
    redLeds[i] = CRGB::Black;
    greenLeds[i] = CRGB::Black;
    blueLeds[i] = CRGB::Black;
    delay(100);
  }
}
```

Notice how, this time, in our loop, we have to write data into each of the three led arrays, since we want different things showing on each led strip.  Now, what if you wanted to programatically choose which led strip you were writing a color value to?  Well, that brings us to our next example, the array of led arrays.

Array of led arrays
-------------------

Now let's get a little fancier.  In order to make a dot that moves from one led strip to the next using the example above, you'd have to have some really ugly code to "pick" the current strip you were writing to.  Or a lot of duplicated code.  That's never any fun.  Instead, here's a technique for using an array of arrays.  Where before you had individual CRGB arrays of leds, now you have an array of CRGB arrays of leds (this example is in Examples, under Multiple/ArrayOfLedArrays):

```C++
#include "FastLED.h"
#define NUM_STRIPS 3
#define NUM_LEDS_PER_STRIP 60
CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];
```

This has set up a two dimensional array.  If you want to access the first led on the first strip, you would use ```leds[0][0]```.  If you wanted to access the third led on the second strip, you would use ```leds[1][2]``` and so.  Setup looks mostly the same, except now we have to tell it which array to use for each strip:

```C++
void setup() {
  FastLED.addLeds<NEOPIXEL, 10>(leds[0], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 11>(leds[1], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<NEOPIXEL, 12>(leds[2], NUM_LEDS_PER_STRIP);

}
```

Now, in the loop, instead of just looping over the leds, we can also loop over the strips.  This code will generate a dot that moves down the first strip, then the second strip, and finally the third strip:

```C++
void loop() {
  // This outer loop will go over each strip, one at a time
  for(int x = 0; x < NUM_STRIPS; x++) {
    // This inner loop will go over each led in the current strip, one at a time
    for(int i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      leds[x][i] = CRGB::Red;
      FastLED.show();
      leds[x][i] = CRGB::Black;
      delay(100);
    }
  }
}
```

One array, many strips
-----------------------

Maybe you don't want an array of arrays.  Maybe you have patterns that just want one single array with all the leds, and let the library figure out where in that array the data for each strip is.  Once again, we setup our led data (this example is in Multiple/MuiltipleStripsInOneArray):

```C++
#include "FastLED.h"

#define NUM_STRIPS 3
#define NUM_LEDS_PER_STRIP 60
#define NUM_LEDS NUM_LEDS_PER_STRIP * NUM_STRIPS

CRGB leds[NUM_STRIPS * NUM_LEDS_PER_STRIP];
```

Notice this time, we still have only one led array, but this time it is large enough to contain information on all the leds in all the strips (180 leds in total).  We'll also be using a slightly modified version of the addLeds method.  This method takes 3 arguments, the led array, an offset into that array (think of this as where the strip being added starts in the array), and how many leds there are.  So, in the example below, the strip on pin 10 starts at offset 0 and has 60 leds, the strip on pin 11 starts at offset 60 and also has 60 leds, and finally, the strip on pin 12 starts at offset 120 and also has 60 leds.

```C++
void setup() {
  // tell FastLED there's 60 NEOPIXEL leds on pin 10, starting at index 0 in the led array
  FastLED.addLeds<NEOPIXEL, 10>(leds, 0, NUM_LEDS_PER_STRIP);

  // tell FastLED there's 60 NEOPIXEL leds on pin 11, starting at index 60 in the led array
  FastLED.addLeds<NEOPIXEL, 11>(leds, NUM_LEDS_PER_STRIP, NUM_LEDS_PER_STRIP);

  // tell FastLED there's 60 NEOPIXEL leds on pin 12, starting at index 120 in the led array
  FastLED.addLeds<NEOPIXEL, 12>(leds, 2 * NUM_LEDS_PER_STRIP, NUM_LEDS_PER_STRIP);

}
```

Now, take a look at the loop method.  We're still moving a dot down each strip, one strip at a time - but there's only one loop, going over all the leds:

```C++
void loop() {
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Red;
    FastLED.show();
    leds[i] = CRGB::Black;
    delay(100);
  }
}
```

Managing your own output
------------------------

FastLED helpfully writes to all the leds strips every time you call show.  However, sometimes, that might not be what you want.  For example, you may want to split leds over multiple lines to conserve memory.  In this case, you can sidestep fastled's automatic display (at the cost of easy global brightness management).  Here's a quick example:

```C++
#include "FastLED.h"

#define NUM_LEDS 80
#define NUM_STRIPS 4

CRGB leds[NUM_LEDS];
CLEDController *controllers[NUM_STRIPS];
uint8_t gBrightness = 128;

void setup() { 
  controllers[0] = &FastLED.addLeds<WS2812,1>(leds, NUM_LEDS);
  controllers[1] = &FastLED.addLeds<WS2812,2>(leds, NUM_LEDS);
  controllers[2] = &FastLED.addLeds<WS2812,10>(leds, NUM_LEDS);
  controllers[3] = &FastLED.addLeds<WS2812,11>(leds, NUM_LEDS);
}

void loop() { 
  // draw led data for the first strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Red);
  controllers[0]->showLeds(gBrightness);

  // draw led data for the second strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Green);
  controllers[1]->showLeds(gBrightness);

  // draw led data for the third strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Blue);
  controllers[2]->showLeds(gBrightness);

  // draw led data for the first strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::White);
  controllers[3]->showLeds(gBrightness);
}
```

Now you can write led data one strip/pin at a time. 

Or, alternatively (using some new pieces added recently to the FastLED object):

```
 #include "FastLED.h"

#define NUM_LEDS 80
#define NUM_STRIPS 4

CRGB leds[NUM_LEDS];
uint8_t gBrightness = 128;

void setup() { 
  FastLED.addLeds<WS2812,1>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812,2>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812,10>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812,11>(leds, NUM_LEDS);
}

void loop() { 
  // draw led data for the first strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Red);
  FastLED[0].showLeds(gBrightness);

  // draw led data for the second strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Green);
  FastLED[2].showLeds(gBrightness);

  // draw led data for the third strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::Blue);
  FastLED[3].showLeds(gBrightness);

  // draw led data for the first strand into leds
  fill_solid(leds, NUM_LEDS, CRGB::White);
  FastLED[4].showLeds(gBrightness);
}
```
