

```
d2 0.7.1
Usage:
  d2 [--watch=false] [--theme=0] file.d2 [file.svg | file.png | file.pdf | file.pptx | file.gif | file.txt]
  d2 layout [name]
  d2 fmt file.d2 ...
  d2 play [--theme=0] [--sketch] file.d2
  d2 validate file.d2

d2 compiles and renders file.d2 to file.svg | file.png | file.pdf | file.pptx | file.gif | file.txt
It defaults to file.svg if an output path is not provided.

Use - to have d2 read from stdin or write to stdout.

See man d2 for more detailed docs.

Flags:
  -w, --watch                       $D2_WATCH               watch for changes to input and live reload. Use $HOST and $PORT to specify the listening address.
                                                            (default localhost:0, which will open on a randomly available local port). (default false)
  -h, --host string                 $HOST                   host listening address when used with watch (default "localhost")
  -p, --port string                 $PORT                   port listening address when used with watch (default "0")
  -b, --bundle                      $D2_BUNDLE              when outputting SVG, bundle all assets and layers into the output file (default true)
      --force-appendix              $D2_FORCE_APPENDIX      an appendix for tooltips and links is added to PNG exports since they are not interactive. --force-appendix adds an appendix to SVG exports as well (default false)
  -d, --debug                       $DEBUG                  print debug logs. (default false)
      --img-cache                   $IMG_CACHE              in watch mode, images used in icons are cached for subsequent compilations. This should be disabled if images might change. (default true)
  -l, --layout string               $D2_LAYOUT              the layout engine used (default "dagre")
  -t, --theme int                   $D2_THEME               the diagram theme ID (default 0)
      --dark-theme int              $D2_DARK_THEME          the theme to use when the viewer's browser is in dark mode. When left unset -theme is used for both light and dark mode. Be aware that explicit styles set in D2 code will still be applied and this may produce unexpected results. We plan on resolving this by making style maps in D2 light/dark mode specific. See https://github.com/terrastruct/d2/issues/831. (default -1)
      --pad int                     $D2_PAD                 pixels padded around the rendered diagram (default 100)
      --animate-interval int        $D2_ANIMATE_INTERVAL    if given, multiple boards are packaged as 1 SVG which transitions through each board at the interval (in milliseconds). Can only be used with SVG exports. (default 0)
      --timeout int                 $D2_TIMEOUT             the maximum number of seconds that D2 runs for before timing out and exiting. When rendering a large diagram, it is recommended to increase this value (default 120)
  -v, --version                                             get the version (default false)
  -s, --sketch                      $D2_SKETCH              render the diagram to look like it was sketched by hand (default false)
      --stdout-format string                                output format when writing to stdout (svg, png, ascii, txt, pdf, pptx, gif). Usage: d2 input.d2 --stdout-format png - > output.png (default "")
      --browser string              $BROWSER                browser executable that watch opens. Setting to 0 opens no browser. (default "")
  -c, --center                      $D2_CENTER              center the SVG in the containing viewbox, such as your browser screen (default false)
      --scale float                 $SCALE                  scale the output. E.g., 0.5 to halve the default size. Default -1 means that SVG's will fit to screen and all others will use their default render size. Setting to 1 turns off SVG fitting to screen. (default -1)
      --target string                                       target board to render. Pass an empty string to target root board. If target ends with '*', it will be rendered with all of its scenarios, steps, and layers. Otherwise, only the target board will be rendered. E.g. --target='' to render root board only or --target='layers.x.*' to render layer 'x' with all of its children. (default "*")
      --font-regular string         $D2_FONT_REGULAR        path to .ttf file to use for the regular font. If none provided, Source Sans Pro Regular is used. (default "")
      --font-italic string          $D2_FONT_ITALIC         path to .ttf file to use for the italic font. If none provided, Source Sans Pro Regular-Italic is used. (default "")
      --font-bold string            $D2_FONT_BOLD           path to .ttf file to use for the bold font. If none provided, Source Sans Pro Bold is used. (default "")
      --font-semibold string        $D2_FONT_SEMIBOLD       path to .ttf file to use for the semibold font. If none provided, Source Sans Pro Semibold is used. (default "")
      --font-mono string            $D2_FONT_MONO           path to .ttf file to use for the monospace font. If none provided, Source Code Pro Regular is used. (default "")
      --font-mono-bold string       $D2_FONT_MONO_BOLD      path to .ttf file to use for the monospace bold font. If none provided, Source Code Pro Bold is used. (default "")
      --font-mono-italic string     $D2_FONT_MONO_ITALIC    path to .ttf file to use for the monospace italic font. If none provided, Source Code Pro Italic is used. (default "")
      --font-mono-semibold string   $D2_FONT_MONO_SEMIBOLD  path to .ttf file to use for the monospace semibold font. If none provided, Source Code Pro Semibold is used. (default "")
      --check                       $D2_CHECK               check that the specified files are formatted correctly. (default false)
      --no-xml-tag                  $D2_NO_XML_TAG          omit XML tag (<?xml ...?>) from output SVG files. Useful when generating SVGs for direct HTML embedding (default false)
      --salt string                                         Add a salt value to ensure the output uses unique IDs. This is useful when generating multiple identical diagrams to be included in the same HTML doc, so that duplicate IDs do not cause invalid HTML. The salt value is a string that will be appended to IDs in the output. (default "")
      --omit-version                $OMIT_VERSION           omit D2 version from generated image (default false)
      --ascii-mode string           $D2_ASCII_MODE          ASCII rendering mode for text outputs. Options: 'standard' (basic ASCII chars) or 'extended' (Unicode chars) (default "extended")


Subcommands:
  d2 layout - Lists available layout engine options with short help
  d2 layout [name] - Display long help for a particular layout engine, including its configuration options
  d2 themes - Lists available themes
  d2 fmt file.d2 ... - Format passed files
	d2 play file.d2 - Opens the file in playground, an online web viewer (https://play.d2lang.com)
  d2 validate file.d2  - Validates file.d2

```

