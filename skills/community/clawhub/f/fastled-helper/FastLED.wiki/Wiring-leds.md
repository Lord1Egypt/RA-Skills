# Introduction 

Obviously, before you can go about writing LED programs you need to have some LEDs hooked up to your arduino.  This page proves some notes and tips for hooking up said LEDs.

# The Wires 

Most modern LED chipsets come with 3 or 4 pins or connectors on them.  Some chipsets, like the WS2801, use 4 pins: Power, Ground, Data, and Clock.  Others, like the WS2812B only use three: Power, Ground, and Data.  Note that Power and Ground are always present.  These wires are what supply power to the LEDs and allow them to light up.  The Data pin is how led data gets from your arduino or micro controller to the actual LEDs.  Finally, for some chipsets, the clock pin is used in conjunction with the data pin for transmitting data.  See the [ChipsetOverview Chipset Overview] page for specific information on the various chipsets and what they use.

# Connecting the wires 

The data and clock pins connect to their appropriate pins on the arduino.  There's a variety of ways to do this, depending on the specifics of your controller.  You can use jumper cables, screw terminals, solder wires directly, etc...

The power and ground pins connect to positive(+) and negative(-) on your power supply to get power to the LEDs.  This should also be pretty straightforward.

In some instances, you may also need to connect ground from the led strips to a ground pin on the arduino.  This can help with keeping the data signal nice and clean.

# A Word on Power 

LED strips and pixels usually come in one of two varieties - 5 volt (also called 5v) and 12 volt (also called 12v).  Be aware of what voltage your LED pixels want!  Plugging a 12v power supply into the power/ground pins of a 5v strip of led pixels may damage your LED strip.  Also - be aware of the power and ground connections.  Power should go to Positive(+) on your power supply and Ground should go to Negative(-).  While some chipsets may protect against accidentally wiring this backwards, many more done and, once again, doing so may damage your chips.

The brighter your LEDs are run, the more power they are going to draw.  Many arduino devices have a 5v power pin, and it is often tempting to just connect a line from there to your LEDs.  However, it is very easy for LEDs to draw a lot of current, more than the arduino can push through its 5v line.  The end result may either be your LEDs not being as bright as you like, or perhaps glitching out and glowing a dim red instead of the colors you want, or worse, possibly damaging your arduino by attempting to draw too much current through and burning something out on the board.

It is generally considered much better to wire power to the leds independently of the arduino.  Most easily, this is done with a splitter from your power supply - with one power lead going to the arduino and the other power lead going to your leds.  This will ensure that everything gets all the power that it wants!