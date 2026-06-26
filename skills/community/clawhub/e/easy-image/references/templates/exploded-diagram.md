# Exploded Diagram

## Use Cases
- Product structure introduction
- Educational anatomy visualization
- Technical documentation
- Marketing materials showing internal components
- Assembly/disassembly guides
- Premium product showcase

## Trigger Keywords
exploded, breakdown, anatomy, structure, components, disassembly, internals, teardown, cutaway, parts, composition, construction

## Defaults
- Aspect ratio: 4:3 (standard infographic)
- Style: Premium/Scientific
- Background: Dark gray studio
- Lighting: Soft studio lighting

## Core Elements
| Element | Required | Default | Description |
|---------|----------|---------|-------------|
| Subject | Yes | - | Main object to show (product, animal, machine) |
| Components | No | Auto-detect | Key parts to separate and display |
| Background | No | Dark gray | Studio background color |
| Annotation | No | Yes | White lines with labels |
| Style | No | Premium | Visual style preset |

## Style Presets

### Premium/Scientific
- Use for: High-end product showcase, educational materials, medical/anatomical visualization
- Features: Clean separated components, floating elements, thin annotation lines, premium poster feel
- Template: `Create a high-end educational exploded infographic showing {subject}. Present the complete, intact {subject} with realistic textures in a studio setting against a dark gray background. Display the internal structure using an exploded view approach where key components float separately around the main body. Arrange internal elements as clean, distinct pieces positioned around the subject. Add thin white annotation lines pointing to each part with small, legible labels. The composition should feel like a premium medical or scientific poster. Render in photorealistic 3D style with soft studio lighting. Keep the visualization clean and elegant without any gore or graphic content.`

### Technical/Engineering
- Use for: Mechanical products, electronics, assembly guides, technical documentation
- Features: Precise separation, numbered parts, engineering blueprint feel, technical accuracy
- Template: `Create a technical exploded view diagram of {subject} in an engineering documentation style. Separate all components precisely and arrange them floating in perfect alignment to show how they assemble together. Number each part and connect them with thin leader lines. Use a dark blue-gray technical background and render from an isometric perspective. The quality should match CAD engineering visualizations with mechanical precision. Ensure all parts are clearly visible and properly labeled in a professional technical illustration style.`

### Minimalist/Marketing
- Use for: Consumer electronics marketing, product launches, advertising materials
- Features: Clean white background, dramatic lighting, fewer components, marketing appeal
- Template: `Create a minimalist exploded product view of {subject} for marketing purposes. Place the product on a pure white background with its key components elegantly separated and floating in space. Use dramatic studio lighting with soft shadows to create visual depth. Focus on displaying only the most important internal features rather than every component. The style should be clean and modern, similar to Apple product visualizations, with premium advertising quality.`

### Anatomical/Educational
- Use for: Biological subjects, medical education, veterinary materials, science illustrations
- Features: Realistic textures, labeled organs/systems, scientific accuracy, educational clarity
- Template: `Create an educational anatomical exploded infographic of {subject}. Show the complete, intact {subject} with realistic texture standing in a studio with a dark gray background. Present the anatomy using an exploded view where the skeletal structure floats above, and internal organs are displayed as clean, separate elements arranged around the body. Show one limb with exposed muscle structure and another with visible bone structure. Add thin white annotation lines pointing to each anatomical part with clear labels. Render in photorealistic style with soft studio lighting. Keep the visualization scientific and elegant without any gore or blood.`

### Layered/Stacked
- Use for: Multi-layer products, sandwiches, mattresses, composite materials
- Features: Vertical separation, layer-by-layer breakdown, cross-section alternative
- Template: `Create a layered exploded view of {subject} showing how it is constructed. Separate the components vertically to reveal each layer, arranging them in a floating stack formation. Each layer should be clearly visible with thin annotation lines identifying the materials or components. Use a dark gradient background with soft studio lighting. The style should be clean and modern, suitable for both technical documentation and marketing materials.`

## Completion Rules
- **Subject not provided**: Request user to specify - this is required
- **Components not specified**:
  - Electronics → PCB, battery, screen, casing, buttons
  - Mechanical → gears, motors, housing, bearings
  - Biological → skeleton, organs, muscles, nerves
  - Food → layers, ingredients, packaging
- **Background not specified**: Default to dark gray for premium feel
- **Annotation not specified**: Default to yes with white lines
- **Style not specified**:
  - Tech products → Technical/Engineering or Minimalist/Marketing
  - Living things → Anatomical/Educational
  - Layered items → Layered/Stacked
  - General → Premium/Scientific

## Specific Presets

### Smartphone Exploded
- Template: `Create a technical exploded view of a smartphone. Float the screen above the device, reveal the PCB motherboard underneath, separate the battery to the side, and isolate the camera module, speaker, microphone, and charging port assembly. Arrange all parts in precise alignment as if frozen mid-assembly. Use a dark gray background with thin white annotation lines labeling each component. Render in an engineering visualization style with ultra-detailed 3D quality.`

### Mechanical Watch Exploded
- Template: `Create a luxury exploded view of a mechanical watch. Separate the movement mechanism from the case, showing individual gears and springs floating in precise alignment. Isolate the crystal, dial, and crown assembly. Use a dark premium background with golden accent lighting to highlight the horological details. Add thin annotation lines to identify key components. Render with ultra-high precision to showcase the craftsmanship.`

### Wireless Earbuds Exploded
- Template: `Create an exploded infographic of wireless earbuds. Separate the outer shell to reveal the speaker driver inside, isolate the battery component, show the microphone array, display the charging contacts, and float the PCB main board nearby. Use a dark gradient background with clean annotation labels pointing to each part. Style this as premium consumer electronics marketing material.`

### Athletic Sneaker Exploded
- Template: `Create an exploded view diagram of an athletic sneaker. Separate the upper mesh from the midsole foam layers, isolate the outsole rubber, display the heel counter, float the insole above, and show the lacing system. Expose the cushioning technology within. Use a dark background with a dynamic viewing angle and thin white annotation lines. Style this as sport technology marketing material.`

### Cat Anatomical Exploded
- Template: `Create an educational anatomical infographic of a gray Scottish Fold cat. Show the complete, intact cat with realistic gray fur standing in a studio with a dark gray background. Present the anatomy as an exploded view: float the skull slightly above the head, position the brain above the neck, keep the spine and rib cage partially visible and aligned with the body. Display the internal organs (heart, lungs, liver, stomach, kidneys, intestines) as clean, separate elements arranged around the torso. Show one front leg with exposed muscle structure and one hind leg with visible skeletal structure. Add thin white annotation lines pointing to each anatomical part with small, clear labels. Render in photorealistic style with soft studio lighting. Keep the visualization elegant and scientific without any gore or blood.`

### Dog Anatomical Exploded
- Template: `Create an educational anatomical exploded infographic of a {breed} dog. Show the complete, intact dog with realistic fur texture standing in a studio with a dark gray background. Float the skull and brain above the head, keep the spine visible, and display internal organs as separate clean elements arranged around the body. Show one leg with muscle structure exposed and another with bone structure visible. Add thin white annotation lines with clear labels. Render in photorealistic style with soft studio lighting. Keep the visualization scientific without any gore.`

### Electric Car Battery Exploded
- Template: `Create an exploded view of an electric vehicle battery pack. Separate the battery modules and float them in formation, reveal the cooling system underneath, isolate the BMS circuit board, display the casing components, and show how the cells are arranged. Label high-voltage connectors clearly. Use a dark technical background and style this as automotive engineering visualization with precise annotation lines.`

### Drone Exploded
- Template: `Create an exploded view diagram of a quadcopter drone. Separate the propellers, reveal the motors, open the main body shell to show the flight controller PCB, isolate the camera gimbal, display the battery compartment, show the GPS module, and expose the ESC components. Use a dark background with thin annotation lines. Style this as tech product visualization with engineering precision.`

### Coffee Machine Exploded
- Template: `Create an exploded view of an espresso coffee machine. Separate the water tank, reveal the boiler system, isolate the pump mechanism, display the brewing group, show the portafilter components, float the steam wand assembly, and separate the control panel. Use a dark background and style this as premium home appliance marketing with clear annotations.`

### Headphones Exploded
- Template: `Create an exploded view of over-ear headphones. Separate the ear cups to reveal the drivers inside, show the headband mechanism, isolate the cushion padding, display the cable assembly, and expose the control buttons. Use a dark gradient background with thin white annotation lines. Style this as premium audio equipment marketing material.`

### Human Heart Anatomical
- Template: `Create an educational anatomical exploded view of a human heart. Separate the chambers so they float apart, reveal the valves between them, and display the major vessels (aorta, pulmonary arteries, vena cava) as separate elements. Show the layers of the muscle wall and indicate the electrical conduction system. Use a dark gray medical background with thin white annotation lines and anatomical labels. Render with premium medical illustration quality, maintaining scientific accuracy without any gore.`

### Laptop Exploded
- Template: `Create an exploded view diagram of a laptop computer. Separate the screen assembly from the body, reveal the keyboard deck, float the motherboard above, isolate the RAM and SSD modules, display the battery pack, show the cooling fan system, reveal the speaker units, and expose the trackpad mechanism. Use a dark technical background with thin annotation lines. Style this as tech product engineering visualization.`

### Camera Lens Exploded
- Template: `Create an exploded view of a camera lens. Separate the glass elements to show the optical path through the lens, reveal the aperture blades, display the focusing mechanism, isolate the lens barrel sections, show the image stabilization unit, and float the mount assembly. Use a dark background with thin annotation lines. Style this as precision optics visualization for photography equipment marketing.`

### Gaming Controller Exploded
- Template: `Create an exploded view of a gaming controller. Separate the shell halves, reveal the PCB inside, isolate the analog stick mechanisms, display the trigger assemblies, show the vibration motors, float the battery compartment, and expose the button membrane layers. Use a dark background with thin white annotations. Style this for gaming peripheral marketing with consumer electronics quality.`

### Bicycle Exploded
- Template: `Create an exploded view diagram of a bicycle. Position the frame as the central element with the wheels separated on either side. Float the drivetrain components (chain, gears, pedals) in alignment, isolate the handlebar assembly, display the brake system, and show the saddle and seatpost. Use a dark background with thin annotation lines. Style this as cycling technology visualization for sport equipment marketing.`
