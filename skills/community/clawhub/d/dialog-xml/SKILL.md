---
name: dialog-xml
description: Explains how XML dialogs are used, covering file layout, coordinate rules, widget attributes, command bindings, and GUI color/font theming.
---

# XML Dialog

FlightGear draws its menubar and dialog boxes with PUI (or Canvas plus a compatibility layer in 2024.2 and later), reading PropertyList XML from `$FG_ROOT/gui/`. A dialog becomes reachable when a menubar item fires `dialog-show` with the dialog's `<name>`. Everything below is the practical subset you need to create, wire up, and restyle those files.

## Minimal dialog skeleton

```xml
<PropertyList>
  <name>hello</name>
  <width>150</width>
  <height>100</height>
  <modal>false</modal>
  <draggable>true</draggable>
  <resizable>true</resizable>

  <text>
    <x>10</x>
    <y>50</y>
    <label>Hello, world</label>
  </text>

  <button>
    <x>40</x>
    <y>10</y>
    <legend>Close</legend>
    <binding>
      <command>dialog-close</command>
    </binding>
  </button>
</PropertyList>
```

The root element is always `PropertyList`; the dialog's `name` lives in a child element, not an attribute.

## Coordinates

PUI treats the screen as a fixed **1024×768** canvas regardless of actual resolution. Values are pseudo-pixels.

- Origin is the **bottom-left** corner of the screen, parent dialog, or enclosing group.
- `x` grows left → right; `y` grows bottom → top.
- Omitted `x`/`y` center the object.
- Omitted `width`/`height` inherit the parent container's size. (The upstream doc says "width" for the height default — that is a typo; read it as height.)

## Attributes shared by most objects

| Attribute | Meaning |
|---|---|
| `x`, `y` | Bottom-left position in pseudo-pixels |
| `width`, `height` | Object size in pseudo-pixels |
| `border` | Border thickness; default 2 |
| `color` | Subgroup: `red`, `green`, `blue`, `alpha` |
| `font` | Subgroup: `name` (no `.txf`), `size`, `slant` — size/slant apply to texture fonts only |
| `legend` | Text drawn on the widget itself (e.g. button face) |
| `label` | Text drawn near the widget |
| `property` | Property-tree path bound to the widget's value |
| `binding` | One or more command bindings fired on activation |
| `keynum` | Raw key code that triggers the widget (e.g. `97` for `a`) |
| `key` | Character or symbolic key name (`"a"`, `"Shift-A"`, `"Tab"`, `"F1"`, `"PageDn"`); escape `<`, `>`, `&` as `&lt;`, `&gt;`, `&amp;` |
| `default` | `true` makes this the object activated by Return |
| `visible` | `false` hides the widget and its children with no reserved space |

## Widget catalog

### dialog
Top-level container. Required `<name>`. Extra keys: `modal` (default false), `draggable` (default true), `resizable` (default false), and a `nasal` block with `open`/`close` scripts. Nasal runs in a dialog namespace; `settimer()` and `setlistener()` set in `open` must be torn down in `close` if they should not outlive the dialog.

### group / frame
`group` is an invisible layout container — children position themselves relative to it. `frame` is the same but draws a border and adjustable background. Use them to move blocks of widgets together.

### input
Editable single-line text field. Bind with `property`; the value is read and written through that node.

### text
Read-only label. Add `format` (printf-style) plus `property` to display a live value, e.g. `<format>%-0.4f m</format>`. A `<label>` is still useful as a width placeholder when the property is empty.

### checkbox
Two-state control; binds a boolean `property`.

### button
Push button. `one-shot` (default true) controls whether it pops back up. Attach one or more `binding`s; `dialog-apply` and `dialog-close` are the usual pair. Mark `<default>true</default>` for Return activation.

### combo
Drop-down of fixed choices. Each option is a `<value>` element; bind the selection to `property`.

### list
Scrollable list box with a right-side slider. Same `<value>` children as combo; updates `property` to the selected entry. On `dialog-update` it re-scans the value nodes.

### airport-list
Auto-populated list of every airport FlightGear knows. `property` acts as a search term on `dialog-update`; the selected ICAO goes back into `property` on `dialog-apply`.

### property-list
Navigable view of the global property tree. Fires bindings on selection and returns the selected path in `property` on apply. It only *shows* values — it does not set them. Held-modifier shortcuts: Ctrl+`.` toggles verbose mode, Ctrl+`..` jumps to root, Ctrl+click on a bool toggles it, Shift+`.` dumps that tree level to the terminal. Printed flags mean `r`/`w` read/write protected, `R`/`W` traced, `A`/`U` archive/user-archive, `P` preserved on reset, `T` tied, `Ln` listener count.

### select
Box with arrow buttons cycling through fixed `<value>` entries, bound to `property`.

### slider
Horizontal by default; set `vertical` to true for a column. `min` (0.0) and `max` (1.0) set the range; `step` and `pagestep` enable discrete movement; `fraction` sizes the handle (0..1).

### dial
Circular direction picker. `min`/`max` (0.0/1.0) and `wrap` (default true) shape the behavior; typical use is a 0–360 heading bound to a property.

### textbox
Multi-line buffered text backed by a property node. `slider` sets the scrollbar width, `wrap` toggles line wrapping (default true), `top-line` sets the first visible line (negative values anchor to the last), `editable` enables editing.

### hrule / vrule
Separator lines that stretch to full width/height by default. Thickness comes from `pref-height` (hrule) or `pref-width` (vrule); `color` styles them.

## Menubar entries

`menubar.xml` is a flat sequence of `<menu>` blocks. Each menu has a `<label>` and any number of `<item>` blocks; each item has a `<label>` plus standard bindings. Submenus and checkmarks are not supported by PUI.

```xml
<PropertyList>
  <menu>
    <label>File</label>
    <item>
      <label>Quit</label>
      <binding>
        <command>exit</command>
      </binding>
    </item>
    <item>
      <label>Weather</label>
      <binding>
        <command>dialog-show</command>
        <dialog-name>weather</dialog-name>
      </binding>
    </item>
  </menu>
</PropertyList>
```

Bindings here use the same vocabulary as keyboard, mouse, joystick, and instrument-panel bindings, so any command valid there is valid here. `dialog-show` with `<dialog-name>` matching a dialog's `<name>` is the standard way to open a dialog.

## Theming

`/sim/gui/` is loaded from `style.xml` and holds one `<font>` group and one `<colors>` group.

```xml
<sim>
  <gui>
    <font>
      <name type="string">Helvetica.txf</name>
      <size type="float">15</size>
      <slant type="float">0</slant>
    </font>
    <colors>
      <background>
        <red type="float">0.6</red>
        <green type="float">0.0</green>
        <blue type="float">0.0</blue>
        <alpha type="float">1.0</alpha>
      </background>
    </colors>
  </gui>
</sim>
```

`<name>` is either a built-in bitmap font (`FIXED_8x13`, `FIXED_9x15`, `TIMES_10`, `TIMES_24`, `HELVETICA_10`, `HELVETICA_12`, `HELVETICA_14`, `HELVETICA_18`, `SANS_12B`) or a texture font under `$FG_FONT` (default `$FG_ROOT/Fonts/`).

plib uses six color slots per widget: `background`, `foreground`, `highlight`, `label`, `legend`, `misc`. A widget like `button` consumes the first four and ignores `legend`/`misc`; `text` uses only `label`. Per-element overrides follow the pattern `<widget>-<slot>`, e.g. `button-legend`, `input-misc`.

Resolution order when drawing, say, a button background:

1. Hard-coded plib default
2. Global `background` from `/sim/gui/colors`
3. Global `button-background` if present
4. Inline `<color>` inside the dialog XML

The same four-step merge runs for each slot. Changing `/sim/gui/colors/*` at runtime only takes effect after a GUI re-init, which the `reinit` command with `<subsystem>gui</subsystem>` performs — note it closes all open dialogs.

## Pitfalls worth checking

- The dialog `<name>` must be unique; `dialog-show` looks it up by name, not by file.
- Every `<menu>` needs its closing tag — the upstream example omits it, which breaks the file.
- `edge` cases in sliders and dials: confirm `min < max` and that the bound property is numeric.
- `property-list` reports paths for both dir and value nodes; validate the node kind before writing.
- `visible=false` removes layout space entirely, so don't expect a placeholder gap.
- `key` values containing `<`, `>`, `&` must be XML-escaped; use `keynum` if escaping gets awkward.

## Example: a small weather dialog

```xml
<PropertyList>
  <name>weather</name>
  <width>320</width>
  <height>180</height>
  <modal>false</modal>

  <text>
    <x>10</x>
    <y>150</y>
    <label>Visibility (m)</label>
  </text>

  <slider>
    <x>10</x>
    <y>120</y>
    <width>280</width>
    <property>/environment/visibility-m</property>
    <min>5</min>
    <max>50000</max>
  </slider>

  <checkbox>
    <x>10</x>
    <y>90</y>
    <width>12</width>
    <height>12</height>
    <property>/autopilot/locks/heading</property>
  </checkbox>

  <button>
    <x>10</x>
    <y>20</y>
    <legend>Apply</legend>
    <binding><command>dialog-apply</command></binding>
    <binding><command>dialog-close</command></binding>
    <default>true</default>
  </button>
</PropertyList>
```
