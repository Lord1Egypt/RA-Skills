* [Saturating math](#saturating)
* [Scaling](#scaling)
* [Fast Random Numbers](#random)
* [Easing/Linear Interpolation](#easing)
* [Trig functions](#sin)

<h1 id="saturating">Saturating Math</h1>
...or how I learned to stop worrying and love 0xFF.

One of the new things the library has is a variety of "saturating" math functions. In LED programming (and DSP programming as well), using saturating math can save you lot of code, make your program easier to read, faster to write, and faster executing as well.

## Example: adding two RGB colors 
Say you wanted to 'add' the CRGB color value 'newTint' to an existing led's RGB values.  (Imagine that newTint is (100,50,0) . )   In the past you'd have to do the addition like this to make sure that adding the new values to the existing ones didn't cause 'overflow' beyond one byte:

```
    int newRed =   led[i].r + newTint.r;
    if( newRed   > 255 ) newRed = 255;
    leds[i].r = newRed; 

    int newGreen = led[i].g + newTint.g;
    if( newGreen > 255 ) newGreen = 255;
    leds[i].g = newGreen; 

    int newBlue =  led[i].b + newTint.b;
    if( newBlue  > 255 ) newBlue = 255;
    leds[i].b = newBlue; 
```

## qadd8: eight-bit saturating addition 
The V2 library provides a function that performs a 'saturating add' of two eight-bit numbers.  With eight-bit saturating addition, if the sum exceeds 255, it's automatically clamped to 255.  The 8-bit saturating add function is named qadd8( x, y).  So:

```
    // 100 + 100 = 200
    sum = qadd8( 100, 100); // --> 200
    
    // 200 + 200 = 255
    sum = qadd8( 200, 200); // --> saturated at 255
```

This is extremely useful for adding R, G, and B channel values, because it automatically prevents overflow and wrap-around.  Using qadd8, the code required to add "CRGB newTint" to an existing led value now becomes simpler, with no "if"s:

```
    leds[i].r = qadd8( leds[i].r, newTint.r);
    leds[i].g = qadd8( leds[i].g, newTint.g);
    leds[i].b = qadd8( leds[i].b, newTint.b);
```

Of course, since this 'adding the three led channel colors' case is exactly why we added this function, we also wrapped it up with a bow by added direct support for adding colors into the CRGB class.  So, in fact, you don't have to write any of the code shown above at all!  All you have to write now is this:

```
    leds[i] += newTint;
```
...and the library takes care adding the R, G, and B channels using quadd8's 8-bit saturating method.  You never have to worry about going past 255 or wrapping around!

## Performance 
It's also worth noting that because of the specific assembly language we used implement this, the method that performs "add this CRGB color to that CRGB color, using saturating math" is actually faster and more compact than the original "C" code shown above.

<h1 id="scaling">Scaling operations</h1>

One thing that you often want to do with numbers is scale them down.  The library does this internally for it's global brightness setting, but perhaps you may want to scale down numbers yourself - to do your own fading type effects.  8 bit values go from 0-255, the best way to think of our scaling functions is they let you set a new upper bound, e.g.

```
    scaled = scale8(val, 100);
```

scales the 0-255 value down to a 0-100 value.  There's a variation on ```scale8``` called ```scale8_video``` which has the property that if the passed in value is non-zero, the returned value will be non-zero.  To account for the fact that these values are linear, while human perception is not, there's functions to adjust the dim/brightness of a value from the 0-255 value, linear, to a more perceptual range:

```
   val = dim8_raw(val);
   val = dim8_video(val);
   val = brighten8_raw(val);
   val = brighten8_video(val);
```

<h1 id="random">Fast random numbers</h1>

Sometimes you want a random number, either 8 bit or 16 bit values.  The default random functions provided by the arduino library are a bit on the slow side.  So we have 6 random value functions, 3 8-bit, and 3 16-bit functions that you can use:

```
     random8()       == random from 0..255
     random8( n)     == random from 0..(N-1)
     random8( n, m)  == random from N..(M-1)
 
     random16()      == random from 0..65535
     random16( n)    == random from 0..(N-1)
     random16( n, m) == random from N..(M-1)
```

<h1 id="easing">Easing and Linear Interpolation functions</h1>

 Fast 8-bit "easing in/out" function.

```
     ease8InOutCubic(x) == 3(x^i) - 2(x^3)
     ease8InOutApprox(x) == 
       faster, rougher, approximation of cubic easing
```

Linear interpolation between two values, with the fraction between them expressed as an 8- or 16-bit fixed point fraction (fract8 or fract16).

```
     lerp8by8(   fromU8, toU8, fract8 )
     lerp16by8(  fromU16, toU16, fract8 )
     lerp15by8(  fromS16, toS16, fract8 )
       == from + (( to - from ) * fract8) / 256)
     lerp16by16( fromU16, toU16, fract16 )
       == from + (( to - from ) * fract16) / 65536)
```
 
<h1 id="sin">Trig Functions</h1>

The library also has fast 16bit sin/cos functions.  The input is an "angle" from 0-65535, and the output is a singed 16 bit number from -32767 to 32767.  The 8bit versions take an input "angle" from 0-255, and the output is a unsigned 8 bit number from 0 to 255:

```
    sin16(x);
    cos16(x);
    sin8(x);
    cos8(x);
```