This documentation will walk your through the setup of a FastLED program, as well as provide some information on basic usage of the library, and also provides some basic information on writing code in general.  The documentation here assumes a simple setup of a single strand of leds.  For more involved uses with multiple strands of leds, or mixing up the types of leds, see the advanced documentation.  

## Before you begin

Before you begin working on the code, there's some things that you'll want to have and know.  The first is what LEDs are you using and how many of them will there be?  Next is what pin, or pins will you be putting the leds onto?  For purposes of our example here, let's say we're using Adafruit's Neopixels, and we have a strip of 60 of them, and we're going to use pin 6.

## Setting up the leds

When writing programs for leds, and when writing code in general, I find it quite helpful to use named constants rather than bare numbers for things.  What is easier to read and understand what's going on - ```FastLED.addLeds<4,6>(leds,60);``` or ```FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);```?  There's a couple of reasons for doing this.  One is, as just shown, it makes code a little bit easier to read.  The other is that it means you only have to make changes in one place if you, say, change how many leds you're working with.  

So, with that said, let's throw in the beginning lines of our .ino file:

```
    #include <FastLED.h>
    #define NUM_LEDS 60
    #define DATA_PIN 6
```

So far, what's been written includes the library, sets a macro definition so that anywhere that NUM_LEDS is seen later in the code gets replaced by 60 and the DATA_PIN is set to 6.  Next, we need to set up the block of memory that will be used for storing and manipulating the led data:

```
    CRGB leds[NUM_LEDS];
```

This sets up an array that we can manipulate to set/clear led data.  Now, let's actually setup our leds, which is a single line of code in our setup function:

```
   void setup() { 
       FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
   }
```

This tells the library that there's a strand of NEOPIXEL's on pin 6 (remember, the value that DATA_PIN was set to), and those leds will use the led array ```leds```, and there are NUM_LEDS (aka 60) of them.

For four wire chipsets you have a couple of options.  If you are using the hardware SPI pins for the device that you're building for, then you don't even have to specify the pins:

```
    void setup() { 
        FastLED.addLeds<APA102>(leds, NUM_LEDS);
    }
```

If you are specifying your own pins, you have to specify a clock and a data pin:

```
    void setup() { 
      FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN>(leds, NUM_LEDS);
    }
```

Finally, sometimes you may want to change the data rate that you are running your leds at.  In this case, you'll also need to specify the RGB ordering and the data and clock pins:

```
    void setup() { 
        FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, RGB, DATA_RATE_MHZ(12)>(leds, NUM_LEDS);
    }
```

The above example tells the library to run the APA102's at a 12Mhz data rate instead of the 24Mhz data rate that it will prefer to try for.  

## Writing an led

Making your leds actually show colors is a two part process with this library.  First, you set the values of the entries in the ```leds``` array to whatever colors you want.  Then you tell the library to show your data.  Your animation/code/patterns will pretty much consist of this cycle.  Decide what you want everything to display, set it, then tell the led strip to display it.  Let's do something very simple, and set the first led to red:

```
    void loop() { 
        leds[0] = CRGB::Red; 
        FastLED.show(); 
        delay(30); 
    }
```

That's pretty simple, isn't it?  Now, you have a program that when you push it out to your arduino will set the first led to red.  Over and over again.  

Hmmm, that's kind of boring.  Let's make it blink!

## Changing an led

You can change the value that you set to an led between calls to show, and the next time you call show the new value will get written out.  So, we can set the value of that first led to Red, let it sit there for a second, then set it back to black, let it sit there for a second, and just keep it looping like that, over and over.

```
    void loop() {
      // Turn the first led red for 1 second
      leds[0] = CRGB::Red; 
      FastLED.show();
      delay(1000);
      
      // Set the first led back to black for 1 second
      leds[0] = CRGB::Black;
      FastLED.show();
      delay(1000);
    }
```

## 'Moving' an LED

Now the led is blinking.  That's all well and good, but there's 60 leds in our strip!  The other leds are probably feeling neglected.  What if we moved an LED dot down the length of the strip?  Remember, we have an array of 60 leds, we should be able to do things with them.  Here's a quick thought for having our traveling dot.  We want to set the first led to, say, Blue, show the leds, set that led back to Black, delay a little bit, then start this over with the second led.  And so on, down the line, until we've shown all the leds:

```
    void loop() {
        for(int dot = 0; dot < NUM_LEDS; dot++) { 
            leds[dot] = CRGB::Blue;
            FastLED.show();
            // clear this led for the next time around the loop
            leds[dot] = CRGB::Black;
            delay(30);
        }
    }
```

## Bringing in external controls

Let's do something a little different.  Let's say you have a [potentiometer][pot] hooked up to your arduino on analog pin 2.  That gives a value from 0-1023.  What if we used the value from there to decide how many leds to have on?  We can use the arduino [map][ardmap] function to go from 0-1023 to 0-NUM_LEDS.  Here's what that loop function might look like:

```
    void loop() {
        int val = analogRead(2);
        int numLedsToLight = map(val, 0, 1023, 0, NUM_LEDS);

        // First, clear the existing led values
        FastLED.clear();
        for(int led = 0; led < numLedsToLight; led++) { 
            leds[led] = CRGB::Blue; 
        }
        FastLED.show();
    }
```

Now you have something that will change the number of leds that are on based on what your knob is set to.


[pot]: http://arduino.cc/en/tutorial/potentiometer
[ardmap]: http://arduino.cc/en/Reference/map