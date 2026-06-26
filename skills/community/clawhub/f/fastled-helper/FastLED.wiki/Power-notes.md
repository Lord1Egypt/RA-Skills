Power: tips, troubleshooting, and measurement.

# Troubleshooting 

Often when an LED strip is acting odd, or randomly, there's a power problem.  Here are some things to check and try:
  * See if your animation works properly at a very low setBrightness level (e.g., "32", which is 1/8th brightness), but then goes nuts at higher brightnesses.  If so: you're out of power.
  * See if your animation works properly on a very small number of LEDs, but then starts going nuts when you step up to a larger number. If so, you're out of power (or you have an out-of-RAM problem).
  * If your setup is USB-powered and having trouble, try powering your LED strips from an external (5v) power supply.  Make sure to connect the Ground from the external power supply to the USB-based Ground.  If your animation flickers and goes nuts when exclusively USB powered, but works fine with an external power supply, you were out of power.
  * To be explicit, if you are using multiple power supplies, make sure that all the grounds are connected together

# Tips
Some of these are just good engineering.  Some are just plain voodoo. Use whichever ones that work for you.  
  * At the 'far' end of long LED strips, connect the Data line to Ground.
  * Insert a 200 ohm resistor between the output pins on the microcontroller and the inputs (data, clock) on the LED strip.
  * Use a level-shifter to raise the voltage of the output pins' 3.3 volts to a full 5 volts before sending it into the LED strip's data (and/or clock) inputs.

# Measuring USB power
Here are a few devices that can be used to measure the current drawn from a USB port; all are easy to use, none deliver NASA-grade accuracy -- to say the least.
  * Century USB Power Meter ($30?) http://www.amazon.com/Centech-USB-Power-Meter/dp/B00DAR4ITE (http://www.century-direct.net/N0-08351/)
  * USB power meter with V/A switch ($15-$20?): http://dx.com/p/245604, http://www.amazon.com/Micro-SATA-Cables-Voltage-Current/dp/B005Z1E3IY/,  http://www.amazon.com/PortaPow-Monitor-Multimeter-Ammeter-Chargers/dp/B00DF2485S/, etc.
  * "Charger Doctor" (<$10) http://dx.com/p/235090
  * "Port Pilot PRO" ($75?) http://www.portpilot.net/ and make sure to look for the fancier "Port Pilot PRO", not the regular "Port Pilot [non-pro]"

# Managing power in FastLED 

_(introduced in FastLED3.1.1)_

FastLED allows you to cap the power usage of your leds.  There's two ways to set the max power draw you want.  The first is by specifying the voltage your leds will be running at and the maximum milliamps you want to draw:

```
   // limit my draw to 1A at 5v of power draw
   FastLED.setMaxPowerInVoltsAndMilliamps(5,1000); 
```

The other is to specify the maximum draw you want in watts:

```
   // limit my draw to 5W
   FastLED.setMaxPowerInMilliWatts(5000);
```

Note that at the moment the power management functions are assuming standard(ish) 5v LEDs.  We will be looking to extend this in the future to account for 12v leds, or 5v leds that may have different power draws than the 5050 based stuff that most folks are using today.