<wiki:toc max_depth="2" />

# How to set an LED's color 

There are lots of ways to set an LED's color; this page gives very short examples of several of them.


## Set RGB Color 

Here are six ways to set an LED's RGB color:

 1. set individual R, G, and B fields, the classic way:
```
    leds[i].r = 255; 
    leds[i].g = 68; 
    leds[i].b = 221;
```
 1. set RGB from a single (hex) color code _(v2)_
```
    leds[i] = 0xFF44DD;
```
 1. set RGB from a standard named web/HTML color code _(v2)_
```
    leds[i] = CRGB::HotPink;
```
 1. set RGB using 'setRGB' and three values at once _(v2)_
```
    leds[i].setRGB( 255, 68, 221);
```
 1. copy RGB color from another led _(v2)_
```
    leds[i] = leds[j];
```
 1. use new 'fill_solid', telling it to fill just one led.  _(v2)_  Note that this is a pretty silly way to set one pixel, but it lets us illustrate the existence of fill_solid, a new convenience function the library provides.
```
    fill_solid( &(leds[i]), 1 /*number of leds*/, CRGB( 255, 68, 221) )
```

## Set HSV Color 

Six ways to set an LED's color from HSV (Hue, Saturation, Value).  In general, they mostly involve assigning a CHSV color to a CRGB color; the colorspace conversion happens through an automatic call to hsv2rgb_rainbow.   
It's worth noting that a 'spectrum' and a 'rainbow' are different things; rainbows are more visually color-balanced, and have more yellows and oranges than spectra do.  You probably want to start with 'rainbow', and only switch to 'spectrum' if you have a specific need.

 1. Using a 'rainbow' color with hue 0-255, saturating 0-255, and brightness (value) 0-255 _(v2)_  
```
	// Simplest, preferred way: assignment from a CHSV color
	leds[i] = CHSV( 224, 187, 255);

	// Alternate syntax
	leds[i].setHSV( 224, 187, 255);
```
 1. Setting to a pure, bright, fully-saturated rainbow hue
```
	leds[i].setHue( 224);
```
 1. Using a 'spectrum' color with hue 0-255 _(v2)_  
```
	CHSV spectrumcolor;
	spectrumcolor.hue = 		222;
	spectrumcolor.saturation = 	187;
	spectrumcolor.value = 		255;
	hsv2rgb_spectrum( spectrumcolor, leds[i] );
```
 1. Using a 'spectrum' color with hue 0-191 _(v2)_  
```
	CHSV spectrumcolor192;
	spectrumcolor192.hue = 		166;
	spectrumcolor192.saturation = 	187;
	spectrumcolor192.value = 	255;
	hsv2rgb_raw( spectrumcolor192, leds[i] ); //raw
```
 1. use new 'fill_solid', telling it to fill just one led.  _(v2)_  Note that this is a pretty silly way to set one pixel, but it lets us illustrate the existence of fill_solid, a new convenience function the library provides.
```
	fill_solid( &(leds[i]), 1 /*number of leds*/, CHSV( 224, 187, 255) );
```
 1. With fill_rainbow.  _(v2)_  Note that this is a pretty silly way to set one pixel, but it lets us illustrate the existence of fill_rainbow, a new convenience function the library provides.
```
	fill_rainbow( &(leds[i]), 1 /*led count*/, 222 /*starting hue*/);
```


## Read RGB Data From Serial 
A "CRGB" is nothing more than a convenient wrapper for three bytes of raw RGB data: one byte of red, one byte of green, and one byte of blue.  You are welcome, and invited, to directly access the underlying memory.  These examples show how you read binary RGB data directly from a Serial stream into your array of LED values:
 1. Read a single pixel of RGB data directly into one CRGB _(v2)_.  
```
    Serial.readBytes( (char*)(&leds[i]), 3); // read three bytes: r, g, and b.
```
 1. Read a whole strip's worth of RGB data directly into the leds array at once _(v2)_
```
    Serial.readBytes( (char*)leds, NUM_LEDS * 3);
```
