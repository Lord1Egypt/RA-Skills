### Interrupt Problems

_(Or, why do I lose (serial|IR|servo) data?)_

If you are using a 3-wire led chipset, (aka Neopixels, WS2812, TM1809), you may have run into some problems when trying to pair it with reading serial data, wifi (for example, on an esp8266), or using i2c, or other libraries.  

The problem is, in a nutshell, interrupts.

Writing out WS2812 data requires some pretty tight timing.  Tight enough that FastLED disables interrupts while it is writing out led data.  This means that while the led data is being written out, any interrupts that happen will be delayed until all the led data is written out.  How long will that be for?  Depends on the number of leds.  WS2812 led data takes 30µs per pixel.  If you have 100 pixels, then that means interrupts will be disabled for 3000µs, or 3ms.  

_What does this practically mean, however?_

Let's say you are using an AVR based arduino and you are reading serial data at 57.6kbps.  The AVR has a single byte serial receive buffer.  Which means it can hold one byte of received data while it is receiving the next byte of data.  If your code hasn't read that byte of data before the new byte finishes being read, it will get lost.  The way this is most often handled is with an interrupt.  This interrupt gets triggered every time a byte finishes being read.  The interrupt handler then copies the byte out of the receive buffer into a (hopefully larger) buffer elsewhere in memory.  

At 57.6kbps you will receive 5760 bytes per second.  Or, put differently, one byte every 174µs.  This means that when a byte of serial data comes in you have 174µs in which to move that byte out of the serial receive buffer before the next incoming byte over writes it.  Remember above, though, that interrupts are disabled while writing out WS2812 led data, and that each pixel takes 30µs to write.  This means that if you have more than 5 leds, it's going to be more than 174µs between when that interrupt is allowed to fire.  Then you lose data, and everyone is sad.  (;_;)

_So what do I do?_

In an ideal world, you would move to a 4-wire led chipset, like the APA102 or LPD8806.  Because these chipsets don't have the WS2812 timing requirements, they don't need to have interrupts disabled while writing data out, and this problem never happens.

In a less than ideal world, you could move to the teensy 3.x or the arduino due.  These are ARM based systems that have far more clock cycles per second available to them.  On these platforms, FastLED will briefly re-enable interrupts between each pixel, to allow handlers to run.  As long as those interrupt handlers don't take more than 5µs to run, everything will be happy.  As long as your interrupt handlers don't need to run more frequently than once every 30µs, that is.

_What if my frames are getting cut short, because interrupts are still running too long - or i'm getting other weird behavior?_ 

Well, then you have a choice - you can either fully disable interrupts while writing out led data by putting the line:

```
#define FASTLED_ALLOW_INTERRUPTS 0
```

before you `#include <FastLED.h>`.  Sometimes, especially on the esp8266, you might have better luck by just tweaking the re-try attempt code with:

```
#define FASTLED_INTERRUPT_RETRY_COUNT 1
```

before you `#include <FastLED.h>`

Another possibility is to split your leds into multiple shorter strips of leds, which would allow you to have even shorter periods of time with interrupts disabled (and/or not having to worry as much about frame writing being interrupted by long interrupts if you have them enabled)

_And if I'm stuck with WS2812's and AVR?_

If you are stuck with the hardware, all is not lost, at least not for reading in serial data.  (Note: If the lack of serviceable interrupts is causing problems for servos, you are out of luck - make one of the hardware switches mentioned above, or use a dual-controller setup where one avr talks to servos, and the other avr talks to the leds - also some folks have had luck using this to drive their servos - https://learn.adafruit.com/neopixels-and-servos/the-ticoservo-library).

The trick is to be a bit more careful/thoughtful in how you're receiving your serial data.

The best way to do things is to switch to a protocol where your arduino _asks_ for data when it's ready.  There's two ways to do this.  The first way is to have the arduino send something over serial when it's in a place to receive data.  Then it waits for a little bit to see if the other side has anything to send, and if it does, it reads the all the data that it can before doing more LED work.  The second way is somewhat similar to this, except instead of sending something over serial when you're ready to receive data instead you raise a pin high indicating that it's ok for the other side to be sending data.

For example:

```
void loop() { 
  uint8_t cmd_buffer[64];
  // Tell the other side to send data
  Serial.println("OK");  
  // Read a pre-determined amount of data
  Serial.readBytes(cmd_buffer, 64); 
  // do stuff with the read data 

  // now do led stuff

  FastLED.show();
}
```

One downside to this is that you could end up spending a lot of time sending data when there isn't really data to send.  A way you could change this is make it so that when the Arduino sends its "OK" to get more data, the first byte the other side sends back is a count of how many bytes of data there is.  If there's nothing new to send, then it'll just send back 0:

```
void loop() {
  uint8_t cmd_buffer[64];
  uint8_t size;

  Serial.println("OK");
  size = Serial.read();
  if(size) { 
    Serial.readBytes(cmd_buffer, size);
    // handle the new data that came in
  }

  // the rest of your normal loop
}
```

Let's say you don't want a back and forth like this however.  What if instead you wanted to have something just continually sending data?  (E.g. boblight/ambilight/adalight).  Then what you can do is make sure that every "batch" of data begins with a known string of bytes called a header.  Let's say that every batch of led data will begin with four bytes - 0xDEADBEEF.  

Now, what we do is we read serial data until we see those four bytes in a row, then we read our full frame of data.  The extra trick is that after we're done calling show, we flush the serial read buffer entirely to make sure we don't have a partial frame of data.  For example:

```
const uint8_t header[4] = { 0xDE, 0xAD, 0xBE, 0xEF };

void loop() {
  // we're going to read led data directly from serial, after we get our header
  while(true) {
    while(Serial.available() == 0){} // wait for new serial data
    uint8_t b = Serial.read();
    bool looksLikeHeader = false;
    if(b == header[0]) {
      looksLikeHeader = true;
      for(int i = 1; looksLikeHeader && (i < sizeof(header)); i++) {
        while(Serial.available() == 0){} // wait for new serial data
        b = Serial.read();
        if(b != header[i]) {
          // whoops, not a match, this no longer looks like a header.
          looksLikeHeader = false;
        }
      }
    }

    if(looksLikeHeader) {
      // hey, we read all the header bytes!  Yay!  Now read the frame data
      int bytesRead = 0;
      while(bytesRead < (NUM_LEDS *3)) {
        bytesRead += Serial.readBytes(((uint8_t*)leds) + bytesRead, (NUM_LEDS*3)-bytesRead);
      }
      // all bytes are read into led buffer. Now we can break out of while loop
      break;
    }
  }

  // now show the led data
  FastLED.show();

  // finally, flush out any data in the serial buffer, as it may have been interrupted oddly by writing out led data:
  while(Serial.available() > 0) { Serial.read(); }

}
```

_What's known to work and where?_

* Someone filed #435 to let us know that IRRemote works on the teensy 3.x.