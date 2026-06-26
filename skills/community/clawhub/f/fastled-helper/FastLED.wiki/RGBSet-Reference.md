# **UNDER DEVELOPMENT - EVERYTHING IN HERE SUBJET TO CHANGE AND/OR BEING WRONG**

### Introducing CRGBSet ###

Up until now, everyone has been used to using a standard C array to access their RGB objects.  This lets you do things like the following:

```
for(int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB::Red; FastLED.delay(33); leds[i] = CRGB::Black; }
```

This moves a simple red dot down the line of leds.  What if you wanted to make the dot two pixels wide?  You used to have to do something like this:

```
for(int i = 0; i < NUM_LEDS-1; i++) { 
  leds[i] = CRGB::Red; 
  leds[i+1] = CRGB::Red;
  FastLED.delay(33); 
  leds[i] = CRGB::Black; 
  leds[i+1] = CRGB::Black;
}
```

Now, though, FastLED is adding a new container class, ```CRGBSet``` which allows you to work on portions of your led array in one shot.  For example, if you want a 2 led wide dot, assuming ```leds``` is a ```CRGBSet``` you can just do:

```
for(int i = 0; i < NUM_LEDS-1; i++) { leds(i,i+1) = CRGB::Red; FastLED.delay(33); leds(i,i+1) = CRGB::Black; }
```

If you could do it to an individual pixel before, you can do it to a set of pixels now.  In addition, ```CRGBSet``` can be passed into most places where you currently pass in ```CRGB*```.  So, starting at the beginning, with creating a CRGBSet - here's a simple demo program:

```
#include <FastLED.h>
#define NUM_LEDS 40

CRGBArray<NUM_LEDS> leds;

void setup() { FastLED.addLeds<APA102>(leds, NUM_LEDS); }
void loop() { static uint8_t hue=0; leds.fill_rainbow(hue++); FastLED.delay(30); }
```

This simply fills a rainbow in on the main ```CRGBSet``` called ```leds```.  What if you want a mirrored type effect?  You could replace your loop line with something like this:

```
void loop() { 
  static uint8_t hue=0;
  leds(0,NUM_LEDS/2 - 1).fill_rainbow(hue++);  // fill the first 20 items with a rainbow
  leds(NUM_LEDS/2, NUM_LEDS-1) = leds(NUM_LEDS/2-1,0);
  FastLED.delay(30);
}
```

```CRGBSet``` is a _reference_ object.  It doesn't have any actual pixel data of its own, rather, it's a reference to some set of other pixel data.  How do you get other pixel data in there?  There's a couple of ways.  The first is you can have a pointer to CRGB objects or an array of CRGB objects that you then use to make your initial set out of.  For example:

```
CRGB *realleds[NUM_LEDS];
CRGBSet leds(realleds, NUM_LEDS);
```

This creates an RGBSet that references the array of real leds.  Or, alternatively (and preferably, going forward), you can use a type of RGBSet called ```CRGBArray``` - which is an RGBSet that has its own set of pixel data:

```
CRGBArray<NUM_LEDS> leds;
```

Now you can do things on all of your leds - or a subset of leds, quite easily.  For example, you could fade all the leds to black:

```
leds.fadeToBlackBy(40);
```

or you could just do a subset:

```
leds(0,9).fadeToBlackBy(40);
```

If you are using an environment/compiler that supports C++11 (Arduino 1.6.6 for some platforms) you can even use the new ranged for loop to iterate over your pixels:

```
for(CRGB & pixel : leds) { pixel = CHSV(hue++,255,255); }
```

or you could just do something to a subset of your pixels:

```
for(CRGB & pixel : leds(8,10)) { pixel = CRGB::Black; } 
```

(of course, the above is equivalent to just saying ```leds(8,10) = CRGB::Black;``` - but this is just to give the basic idea for how it could be used).  Note that in testing it is _faster_ to use this style of loop vs. the more traditional 

```
for(int i = 0; i < NUM_LEDS; i++) { leds[i] = CHSV(hue++,255,255); }
```

The loop overhead is reduced 10-20% when using CRGBSet iterators.

What's that, you say?  Your compiler doesn't support C++11/14, and you want the faster loops?  Don't worry - it takes a little bit more code to do - but you can get them as well:

```
    for(CRGBSet::iterator pixel=ml.begin(), end=ml.end(); pixel != end; ++pixel) { (*pixel) = CRGB::Black; }
```

I know, it's a little uglier.  Get thee to C++11!

This is a work in progress - you can see some more ideas on things you do on the g+ post here - https://plus.google.com/102282558639672545743/posts/a3VeZVhRnqG - and I will try to update this page with more documentation and examples as I work on/expand this functionality.