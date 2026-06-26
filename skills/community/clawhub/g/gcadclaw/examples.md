# GcadClaw Example Prompts

These prompts mirror the runnable examples in `src/pygcadwin/examples`.

## centrifugal-impeller

```text
Create a 2D three-view drawing in millimeters for a centrifugal impeller.
Draw a top view of a 90 mm OD backplate centered at the origin, a front section/elevation showing heights, and a right-side section/detail view for the hub, backplate, and blade stack.
In the top view, show a 26 mm central hub and an 8 mm through-bore.
Show 12 identical backward-curved blades on top of the backplate, equally spaced every 30 degrees, spanning from radius 18 mm to radius 43 mm.
Represent each blade as a curved 3 mm thick 2D profile that sweeps backward by about 45 degrees from root to tip.
Annotate backplate thickness 6 mm, hub height 22 mm above the backplate, blade height 16 mm, 1 mm blade-root fillets, and 1.5 mm backplate OD fillets.
Save as a DWG file.
```

## circular-flange

```text
Create a 2D three-view drawing in millimeters for a circular flange.
Draw a top view of an 80 mm outside diameter flange centered at the origin, a front section through the bore, and a right-side edge view/detail showing thickness and fillets.
Show a central 30 mm vertical through-bore and six equally spaced 6 mm through-holes on a 60 mm bolt-circle diameter.
Annotate the 10 mm thickness and 1.5 mm fillets on the top and bottom outside circular edges.
Save as a DWG file.
```

## clevis-bracket-lightening-cutouts

```text
Create a 2D three-view drawing in millimeters for an aerospace-style clevis bracket.
Draw top, front/elevation, and right-side views of a 120 x 60 x 10 mm base plate centered on the XY origin and symmetric about the XZ plane.
Show two clevis lug footprints near the center, each 18 mm thick in Y, 36 mm long in X, with a 16 mm central gap.
In the front and right-side views, show lugs rising 42 mm above the base and rounded top profiles of radius 18 mm.
Add a Ø14 horizontal clevis hole through both lugs along Y at X = 0 and Z = 34 mm.
Show four Ø7 vertical mounting holes at X = +/-45 mm and Y = +/-20 mm, two triangular lightening cutouts with R3 corner notes, two 6 mm diagonal ribs, R3 base perimeter fillets, and R2 lug-to-base fillets.
Save as a DWG file.
```

## l-bracket

```text
Create a 2D three-view drawing in millimeters for an L-bracket.
Draw top, front/elevation, and right-side views of the 80 x 50 x 8 mm base plate centered on the XY origin and the 80 x 8 mm vertical back plate footprint along positive Y.
Show two Ø6 vertical through-holes in the base at X = +/-25 mm and Y = -10 mm.
In the front/elevation view, show a 50 mm tall back plate with two Ø6 horizontal through-holes at X = +/-25 mm and Z = 30 mm.
Show two triangular gussets at X = +/-20 mm with 30 x 30 mm side profiles and note 2 mm fillets at the base/back outside transition.
Save as a DWG file.
```

## open-top-electronics-enclosure

```text
Create a 2D three-view drawing in millimeters for an open-top electronics enclosure base.
Draw top, front section, and right-side section views of a 100 x 70 mm rectangular enclosure centered on the XY origin, with 3 mm walls and an open top.
Show an inner cavity offset inward by 3 mm and four internal standoffs at X = +/-35 mm and Y = +/-25 mm.
Each standoff has Ø10 outside diameter and a centered Ø3 blind hole, 8 mm deep from its top.
Add section notes for 30 mm outer height, 3 mm floor thickness, standoff height 12 mm above the floor, and 2 mm outside vertical corner fillets.
Save as a DWG file.
```

## planetary-gear-stage

```text
Create a 2D three-view assembly drawing in millimeters for a visually clear simplified planetary gear stage.
Draw a top assembly view in the XY plane, a front section through one planet axis, and a right-side stack-up/detail view with gear axes along Z and separate visual bodies/layers for the sun gear, three planet gears, ring gear, carrier plate, and three planet pins.
Use simplified straight-sided trapezoidal teeth rather than true involute teeth.
Draw the sun gear with 24 external teeth, pitch diameter 48 mm, root diameter 42 mm, outside diameter 54 mm, and a Ø10 central bore.
Draw three planet gears with 18 external teeth each, pitch diameter 36 mm, root diameter 31 mm, and outside diameter 41 mm; place centers on a 42 mm radius circle at 120 degree spacing.
Draw the ring gear concentric with the sun gear with 60 internal teeth, internal pitch diameter 120 mm, internal root diameter 126 mm, tooth-tip diameter 114 mm, and outside diameter 140 mm.
Show the carrier plate below the gears as a Ø105 circle with note Z = -5 to -1 and show three Ø6 planet pins centered under the planets with 14 mm height.
Save as a DWG file.
```

## radial-engine-cylinder

```text
Create a 2D three-view drawing in millimeters for a radial-engine-style cylinder with cooling fins.
Draw top, front/elevation, and right-side section views. In the top view, show the 70 mm base flange, six Ø5 mounting holes on a 56 mm bolt circle, the 36 mm barrel, 62 mm cooling fin OD, 44 mm top cap, and angled spark-plug boss projected outward in +X.
In the side/elevation views, show barrel height 70 mm, 12 horizontal fins that are 2 mm thick and spaced every 5 mm from Z = 10 to 65, an 8 mm thick base flange, and an 8 mm tall top cap from Z = 70 to 78.
Show the spark-plug boss as a Ø12 x 24 mm cylinder angled 35 degrees upward from horizontal with a Ø5 coaxial bore.
Annotate 1 mm fillets on fin and flange outer edges.
Save as a DWG file.
```

## rectangular-calibration-block

```text
Create a 2D three-view drawing in millimeters for a rectangular calibration block.
Draw top, front/elevation, and right-side views of a 100 mm by 60 mm block centered on the XY origin.
Show four vertical through-holes, each 8 mm diameter, at X = +/-35 mm and Y = +/-20 mm.
Annotate that the block thickness is 20 mm and that only the top outside perimeter has a 2 mm chamfer.
Save as a DWG file.
```

## spiral-staircase

```text
Create a 2D three-view assembly drawing in millimeters for a miniature spiral staircase.
Draw a plan view centered on the origin plus front and right-side elevation references.
In plan, show a central Ø14 column, a Ø90 base disk, and 20 wedge-shaped treads with inner radius 10 mm, outer radius 62 mm, and 24 degree angular width.
Arrange the treads helically by rotating each subsequent tread 18 degrees; annotate that each step rises 6 mm and is 4 mm thick, starting at Z = 4 mm.
Draw a helical handrail path projected at radius 66 mm making one full revolution from Z = 14 to Z = 130, and show 20 baluster locations at tread outer ends.
Save as a DWG file.
```

## stepped-shaft-keyway

```text
Create a 2D three-view drawing in millimeters for a stepped shaft with keyway.
Draw front/side, top, and right-end views with the shaft axis along X, left end at X = 0 and total length 120 mm.
Show diameters Ø20 from X 0-30, Ø30 from X 30-90, and Ø20 from X 90-120.
Draw a top keyway slot on the middle section, 6 mm wide in Y, 3 mm deep in Z, from X = 40 to X = 80.
Annotate 1 mm chamfers at both end edges.
Save as a DWG file.
```
