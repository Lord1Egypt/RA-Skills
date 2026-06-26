### Make sure you're using arduino-esp8266 v2.2.0 or later

Use arduino board definitions from http://arduino.esp8266.com/stable/package_esp8266com_index.json - and make sure you're using v2.2.0 or later, this will ensure that pin definitions get set up correctly.

### pin definitions?

There appear to be two major types of pin layouts for ESP8266 boards.  There's a raw layout, where pin 0 is GPIO0, pin 1 is GPIO1, etc... up to pin 16 being GPIO16.  Then there's the NodeMCU layout where pin 0 is GPIO 16, pin 1 is GPIO 5, etc... 

The library will attempt to, based on board definitions, guess the right layout to use.  If it isn't, or if you want to force using a pin to gpio mapping, you can use one of:

```
#define FASTLED_ESP8266_RAW_PIN_ORDER
#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#define FASTLED_ESP8266_D1_PIN_ORDER
```

before you `#include <FastLED.h>` in your .ino file.

### pin limitations

The ESP8266 is a limited platform in some ways.  While, on paper, it has 17 GPIO pins, in reality, 6 of these are blocked off from use.  GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, and GPIO11 are all unavailable to you.  These pins are not defined at all for `FASTLED_ESP8266_RAW_PIN_ORDER`, and the NodeMCU pin ordering already excludes these 6 pins from its list of available pins.

In addition, if you are using Serial input/output at all, attempting to use GPIO1 for leds will cause the device to reset.  

### misc

On some boards, if you want to use GPIO15, you may need to follow the instructions here - http://www.instructables.com/id/ESP8266-Using-GPIO0-GPIO2-as-inputs/?ALLSTEPS