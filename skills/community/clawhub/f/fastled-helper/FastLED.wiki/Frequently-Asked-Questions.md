#### 0. Is there documentation?  Where can I get help?

FastLED is a large, complex library.  It is closer to a framework than a simple library like most Arduino libraries you may be used to using so far.  Documentation and explanation of what the library can do, and how to do complex things with it is an ongoing project/process for us.  However, there are lots of pieces in place:

* [This wiki](http://fastled.io/wiki) - read through the pages on the sidebar here, there's a lot of information in there!
* [API Documentation](https://fastled.io/docs/) - doxygen generated API documentation for the library.  This is more reference than how-to, and is continually being updated/expanded
* [The examples](https://github.com/FastLED/FastLED/tree/master/examples) - FastLED has many examples to show off how to do things in the library.  These are also continually expanding.
* [The Reddit Group](http://fastled.io/r) - FastLED has a large community of active users, many of whom are quite helpful.  The community is open to people of all levels, and we've helped with everything from basics of programming to hardware design, as well as using FastLED.  Feel free to go to the community and do a quick search around to see if other folks have had your problem.
* [The FastLED chatroom](http://fastled.io/chat) - the chat room is a place where some random conversation about FastLED occurs.  

#### 0a. Guidelines for asking for help on the G+ group

* Be complete!  Describe what is going on.  "It doesn't work" isn't helpful.  "The first 10 leds light up, but the remaining 30 don't" is better.
* Did we mention details?  Please also include:
  * The version of the arduino IDE you are using (and what OS you're using)
  * The version of FastLED you are using
  * The LED chipset you are using
  * What hardware you are building for
* Providing a link to your code will get some of the quickest help, as we don't have to guess at how you're trying to do what you're doing.  Please upload your code [gist](http://gist.github.com) so we can read it (code in G+ posts gets unreadable very quickly).  Also please update your entire sketch.  You will often be wrong about where you think the problem is in your code.  Please do _not_ use pastebin anymore, as this appears to cause posts to get auto-moderated by g+... thanks, google.
* [More on asking good questions](http://stackoverflow.com/help/how-to-ask) and [making examples](http://stackoverflow.com/help/mcve)

#### 1. I'm losing serial data when I call FastLED.show(), why?

Short version - you're running into problems with interrupts.  Long version - see the [[Interrupt problems]] wiki page.

#### 2. Help!  When I say leds[0] = CRGB::Red it comes out green!

Not all LED chipsets receive their data in RGB order.  See [[RGB Calibration]] for more info on how to adjust the rgb ordering.

#### 3. Help!  I'm getting a compiler error about "avr/io.h" not being found!

This most likely means that you are compiling for a platform that FastLED doesn't yet support.  Please [check the FastLED issues](http://fastled.io/issues) to see if there's already an issue for your platform, and if not, [make a new issue to add your platform](https://github.com/FastLED/FastLED/issues/new).  

#### 4. Help!  I'm getting weird flickering with my leds, and nothing looks right, why?

First thing to check is the wiring.  Make sure that you have power going to the + (or vcc) line on your leds.  Make sure that you have ground from your power going to the - (or gnd) line on your leds.  Also, make sure that you are running ground to ground on your controller as well, especially if you are running your leds off of a separate power supply than your controller.  Next, check your data lines:

Are your data (or data and clock) lines going to DIN (or DIN and CIN) on the leds?  If you connect the data line from your arduino to the DOUT (data out) pin on your leds, nothing is going to come out right.

Likewise, if you are using a 4-wire chipset like the APA102, if you have connected your clock line to your data line and vice versa, then Weird Stuff™ is going to happen.

#### 4b. I've corrected my wiring but now nothing lights up!

For some LED chipsets, if you accidentally wire ground and power backwards, or if you apply power to DIN, you will blow out the led.  _*You have not destroyed your entire strip of leds*_.  Luckily, you've most likely only damaged the first led in the chain, and you can cut it out and re-connect your wiring to the second led and continue using the rest of the leds.

#### 5. With APA102 leds, my wiring is right, but my leds are flickering.  (Or my leds start flickering somewhere down the line).

APA102 leds allow for high data rates.  I've driven them at 24Mhz+ for nearly 1000 leds.  However, for some reason, some ways of manufacturing APA102 strips have problems with high data rates when the strip is long.  If this happens, you can try slowing down the data rate that FastLED uses to write out APA102 data.  Often, setting it to 12Mhz or 10Mhz works:

```
FastLED.addLeds<APA102,7,11,RGB,DATA_RATE_MHZ(10)>(leds,NUM_LEDS);
```

#### 6. Why doesn't FastLED support this random led chipset or that random MCU?

There's a couple possible reasons why FastLED may not support a particular LED chipset or run on a particular MCU:

* Time - this is actually the most likely reason.  FastLED's primary developers have full time jobs, as well as fairly full plates of led work (personal art, contract development, ongoing FastLED development).  This means the list of things we want to do is growing faster than our ability to work on things.
* Awareness - sometimes we just aren't aware of a new LED chipset or MCU yet.  Feel free to [open an issue](https://github.com/FastLED/FastLED/issues/new) to put something on our radar.
* Technical - some LED chipsets we have made a decision to not directly support in the library.  Primarily this includes any LED chipset that requires interrupts/timers to properly manage/control (HL1606, LPD6803).  FastLED supports multiple AVR variants, as well as nearly a half dozen arm architectures (with a couple architectures that are neither ARM or AVR on the horizon as well) - each of which do interrupts and timers slightly differently.  Likewise, with some MCU architectures we've made a decision to not support because of either time (msp430, for example) or because we don't feel the platform is a useful platform to try to optimize FastLED for (PIC).

#### 7. How many leds can I drive?

This is a question that comes up a lot.  On the surface, it seems like it is a simple question so it should have a simple answer, right?  Unfortunately - wrong.  It's a simple question with a lot of complexity hiding underneath the hood.  To answer this question, there are a number of variables that come into play:

* The controller MCU - what controller are you using, an Arduino uno?  A Leonardo?  A teensy 3.2?  An esp32?  All of these controllers have different amounts of memory, which is the first layer of limiting how many leds you can have, but that isn't all!
* The leds you are using - the leds themselves you are using will also have an impact - because this determines how long it takes to write out a frame, whether or not you can use parallel output to make that faster, etc.. etc.. (and that's not including the power calculations)
* What frame rate you want - how many times a second do you want your animation to update the leds?  5?  30?  60?  144?  The higher the frame rate, the smoother things will appear to human eyes.  Below 30 frames per second there starts being a flicker or stutter that is very noticeable - and there's two pieces that play into the frame rate - one is the LEDs and MCU which will determine, at a low level how many leds per second you can update - and the second one is the MCU and your animation code, because the time that your code spends getting led data ready for the next frame of the animation is time it isn't spending writing out led data.  (There are controllers with DMA options for writing data "in the background" - but there are still some costs at the point that you call FastLED.show() that will impact that, and some of these mechanisms also will still steal cpu time away from your animation code)

So, now that there's all of that, let's play things out a bit further.  In the past, I joked that the answer to this question comes down to math - and it mostly does - and there are two pieces here.  The first is the amount of memory that the MCU you are using has available.  The second is the frame rate that you want, and what output mechanism you are using.

On the memory front - At its simplest, FastLED requires 3 bytes of RGB data per led you have.  So, if you want to have 1000 leds you will need 3000 bytes of ram to store the led data.  Note that this would immediately knock the Arduino Uno out of the running, as it only has 2000 bytes of ram.  "But wait!" you might be saying, "2000 divided by three is 666 so I can have 666 leds!" - not so fast sparky...  Because you also need ram for other things - FastLED uses some internally for housekeeping.  Other libraries you are using may as well.  And then there is ram used for all the things that aren't raw led data.  And finally, the system needs some ram itself for things like storing variables, and information on what code is currently executing, etc... etc...

And then on to the frame rate front.  For this, you start with the minimum number of frames per second that you want (say, 30 frames per second) and then the number of leds you are thinking about, say, 1000.  So, with 1000 leds at 30 frames per second you would need to be able to write out a total of 30,000 leds worth of data per second.  Now, remember where I mentioned you would also want CPU time for
your animation?  Well, the rule of thumb that I like to use is assume that you're going to use 50% of the cpu time building animation frames, and then the rest writing out led data (as a worst case scenario).  So that really means that we'd want to be able to write out 30,000 leds worth of frame data in half a second, or 500ms - or, to put another way, we'd need to be able to write out a single led's worth of data in 16.6µs (microseconds).  

Now we start looking at the leds.  The WS2812, the most popular led chipset used out there by FastLED users (if not the WS2812, then one of it's siblings, the WS2813, WS2815, the APA104, and the SKsomethingorother), takes 1.25µs per bit of data written - and each led has 24 bits of data, which means it takes 30µs to write out a single led's worth of data for the WS2812.  Well, that puts a bit of a damper on the whole 1000 leds at 30 frames per second, doesn't it?   Fine, then for WS2812 leds let's work backwards.  It takes 30µs to write a single led worth of data.  We have 500ms alloted to writing led data, so 500ms (or 500,000µs) divided by the 30µs per led gives us 16,666.  So we can write a total of 16,666 leds worth of data - and at 30 frames per second that gives us (16,666 divided by 30) 555 leds that we can have.

This is where things can start getting fancy.  Sure - at raw numbers that would be true.  However, if you are using something that can do parallel output (for example, the Teensy 3.2 with or without the OctoWS2811 library, or the esp32) then you can play with the numbers a bit.  If you're writing out _two_ leds worth of data at the same time, well, then with the above numbers you could update 1110 leds in 500ms and still have 500ms left over for building your animations.  You could write out _eight_ leds worth at the same time (on the teensy 3.2) and now you're talkinng about 4,440 leds you could update 30 times/second.  And if you, as you can on the esp32, write out _24_ leds worth of data at the same time then you're up over 13,000 leds you could have.

You can juggle these numbers around to give yourself more leds, or more CPU time to do more complicated animations.  At some point I might try putting together an online calculator with sliders that you can use to adjust things like number of leds, frame rate, parallel output, and % cpu time for generating patterns so you can more easily see how these play and interact with each other.
