# The design of FastLED

This is an attempt to document the high level design of the FastLED library, and give some insight to some of the design ideas that went into how everything works and is laid out.  In the future there will be more articles that drill down into the code specifics of how we get some of the performance and features that we do.

## Goals

There are a handful of goals that guide the design of the library.  The first of these is encoded in the name of the library - to be fast.  The second goal is also in the name of the library, which is to support LEDs - as wide a variety of leds as we can.  The third goal is to support multiple multiple microcontroller platforms.  Finally, the fourth goal is to provide as much support for people doing LED programming, at all levels, not just the talking to the leds themselves.

All of the goals  can be wrapped up in one singular meta-goal, to enable people to do LED programming and focus on that, without them having to worry about the specifics of the led chipsets, the controller, performance, etc... etc... etc...

### Fast as a goal

There's multiple meanings for the idea of fast as a goal, and the library tries to hit all of them.  There's "How quickly can someone new to LEDs get up and running with making LEDs do their bidding?", there's "How quickly can the library do it's work", or alternatively, "How much CPU time does the library leave available for the led programmer to spend on their led/animation code?"

Sometimes these two subgoals can be at odds with each other.  The fastest possible way to do things may not be the most straightforward or intuitive for a new user to do.  Sometimes, the easiest way to present/do things is, conversely, not the highest performing way to dothings.

FastLED attempts to address this by exposing multiple layers to the developer.  The highest layer is the one that's designed to be easiest for end users to use.  It turns out, as well, that for most cases, we've been able to make things run pretty damn fast, even at this layer.  Then there's a layer below that, that's slightly more raw components, but these allow more advanced developers to play games and tricks that can lead to higher performance (or ability to support more leds).  Finally, there's the layer below that, which attempts to abstract out hardware access across multiple MCUs, while providing the fastest access to things like pins or SPI hardware interfaces.  

### Wide support as a goal

It turns out that this layering also allows us to make it easier to support multiple platforms as well as multiple LED chipsets.  Because we've abstracted out a lot of the low level hardware access, the higher level code for driving LEDs is rarely platform specific.  Likewise,  because we've abstracted out SPI access, writing controllers for SPI based LED chipsets is also fairly straightforward.  

Of course, to the end user, they don't see/worry about the specifics of different LED chipsets beyond selecting which chipset they are using.  We can add support for more chipsets and people can start using them without having to change any of their code beyond that specifying what chipset they're using.

Right now, the library supports MCUs that use the arduino environment as a dev environment, this includes AVRs from the ATTiny85 all the way up to the ATmega2560, as well as arm chipsets used by the teensy 3 and the due.  We also have a few more arduino environment based chipsets that are on the roadmap to support, which will allow supporting things like the RFDuino and the SparkCore as well.

However, the library is also designed with an eye towards supporting platforms that aren't arduino environment based.  While we haven't gotten to that point yet, platforms like the BeagleBone black are on our list for things to tackle.

### More than just LEDs

There's more to LED programming than just setting the colors of each LED on each frame.  There's a wide variety of math and color transformation options that are useful for the LED programmer to use, and a lot of the methods that people, especially at the "new to this" level, that may not be the most optimal.  To help out with this we have a variety of fast math functions for things like sin/cos, or the specific 8 bit manipulations that one would want to do for adjusting/scaling/changing the RGB values for each pixel.  We even support working in other colorspaces like HSV to give people an even higher level, more abstract way of dealing with color and brightness, giving them a much nicer, smoother look to their color work.

## From the top down - FastLED

Like layers of the onion, now we're going to peel apart the library, starting from the top level, the interfaces that people will see.  There may be small detours here and there to dig into the specific pieces that we have.

There are two top level objects in FastLED that everyone will deal with.  The first of these is the CRGB class.  This is an object that represents a single RGB pixel.  We have supplied a number of methods on this class to allow for rapid modification of the various values in the RGB pixel, allowing one to do things like blend pixels, scale them, or otherwise transform them.  Most people's first interaction with this class will be the declaration of their LED array:

```
CRGB leds[NUM_LEDS];
```

The second object is FastLED itself.  This is a controller.  For each LED 'thing' that you're plugging in, you tell FastLED what chipset is being used, what pin(s) it is being used on, how many LEDs are on it, and what CRGB array to use when writing to that set of leds.

The first place the user will come across this object is in the setup method, when they're setting up their LEDs:

```
void setup() {
	FastLED.addLeds<NEOPIXEL,6>(leds, NUM_LEDS);
}
```

and the second place will be with regular calls to the show method, which tells FastLED to push the data in leds out to the led strips:

```
void loop() { FastLED.show();}
```

When you call show, the FastLED object will loop over all the sets of leds that you have added to itt, and call show on each set of leds, with the appropriate set of leds and other necessary options.  FastLED also provides methods for globally setting the brightness, color correction information, whether or not to use dithering.  Finally, the high level FastLED object provides some methods for filling your leds in fun ways, to get a bit of a kickstart to what you're doing.

## A little bit lower now, CLEDController

When you tell the library to add a strip of NEOPIXELs, you're also, indirectly, telling it what LED controller class to use (in this case, on named NEOPIXEL).  There's a definition for a class called CLEDController that defines the basic methods that all LED controllers will provide, things like show, setColorTemperature, etc...  There are a variety of classes that implement these methods for each of the supported LED chipsets.  For some chipsets, like the SPI based chipsets, the individual, chip specific controller classes are pretty lightweight, as all they do is some basic setup of underlying SPI classes, and provide information on any special data adjustments that each particular chipset may require before data gets written out (for example, the LPD8806 only uses the high 7- bits of your RGB values, in the meantime, the P9813 (aka CoolNeon's Total Control Lighting) prepends each RGB pixel data with a checksum value).  For the 3wire chipsets, the structure is a little different.  There is a platform specific class that defines writing out to the 3-wire chipsets, in general, and each specific chipset's definition provides the platform specific class with timing information for the specific 3 wire chipset.

### Hitting the watertables, platform specific interfaces

For both SPI chipsets and the 3-wire controllers, there are platform specific classes that provide the implementation for talking to those controllers in general.  For example, there is an implementation of an SPI controller for AVR that uses the AVR's hardware SPI controller.  Likewise on the teensy3, using the k20's SPI controller.  In addition, there's an SPI controller that does bitbanging, and finally, there are plans for SPI controllers that use the SPI mode in a variety of MCU's USART controllers as well, to provide more options for hardware accelerated output of led data.  These are pretty low level classes, in some cases, doing direct i/o register manipulation to control the SPI buses, or the performing very exact timing for the 3-wire led chipsets.

There will be other pages/documents in the wiki that will describe in much more detail how these lower level classes work, how they relate to the LED protocols, and the MCUs that someone's code is running on.

### Bedrock, the core, fast pin access.

From the very first implementation, low level, direct access to the underlying hardware has defined the library.  From SPI controller classes that directly interface with control registers and optimize ordering of loading data to fast Pin access classes that, on some platforms turn pin access into a one clock cycle operation.  

The SPI classes live in sort of two spaces.  On the level just above,they provide methods and interfaces that optimize writing led data out and performing the various in stream data manipulations that we do. On the lower level, they are all about direct access to the SPI registers, making aggressive use of method inlining to get the fastest access to the SPI system going.

The FastPin class is a template that takes advantage of the fact that, for most people, the pins being used are known at compile time, and using that information, we can flatten pin access down to direct manipulation of the gpio registers.  When you are trying to push data out as fast as you can, the fastest pin access possible is a good thing to have!
