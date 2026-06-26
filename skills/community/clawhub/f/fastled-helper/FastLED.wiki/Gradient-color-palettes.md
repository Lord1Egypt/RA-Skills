FastLED v3 and later support "color palettes", which map from a single one-byte value (0-255) to a full RGB color.  By populating the 'lookup table' palette with different color schemes, you can give your animation different appearances without changing the underlying code.  Color palettes are traditionally specified as a list of explicit RGB colors, either 256 or 16 of them.

Starting with FastLED v3.1, there's a new way of specifying color palettes: as a series of gradients.  So for example, you could say that you wanted a heatmap palette that faded slowly from black (0,0,0) to red (255,0,0), then to bright yellow (255,255,0) and then quickly to white (255,255,255), like this:

![](https://github.com/FastLED/FastLED/blob/gh-pages/images/gradient-palette-1.png)

You can now specify that palette like this:

    DEFINE_GRADIENT_PALETTE( heatmap_gp ) {
      0,     0,  0,  0,   //black
    128,   255,  0,  0,   //red
    224,   255,255,  0,   //bright yellow
    255,   255,255,255 }; //full white

The first column specifies where along the palette's indicies (0-255), the gradient should be anchored, as shown in the diagram above.  In this case, the first gradient runs from black to red, in index positions 0-128.  The next gradient from red to bright yellow runs in index positions 128-224, and the final gradient from bright yellow to full white runs in index positions 224-255.  Note that you can specify unequal 'widths' of the gradient segments to stretch or squeeze parts of the palette as desired.

Once you've defined a palette like this, here's how to activate it:

    CRGBPalette16 myPal = heatmap_gp;

Note that the palette definition itself is stored in PROGMEM flash storage until loaded into a CRGBPalette16 or CRGBPalette256.  This means that you can have many different gradient palettes defined in your sketch, and activate them one at a time as needed.  Then to select a color from your heatmap palette:

    uint8_t heatindex = (something from 0-255);
    leds[i] = ColorFromPalette( myPal, heatindex); // normal palette access

