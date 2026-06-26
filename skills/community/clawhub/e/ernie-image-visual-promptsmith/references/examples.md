# Examples

Use these examples to calibrate prompt quality and generation settings. They are template-style examples adapted for this skill; do not treat them as official wording.

## Style Category Examples

### Photorealistic

Input: `拍一个商业咖啡杯产品图`

Prompt: Photorealistic close-up commercial product photograph of a matte ceramic coffee mug on a light oak table, cup centered with handle visible, soft morning sunlight from the left, gentle shadow on the right, subtle background blur, visible ceramic texture, clean ecommerce styling, sharp detail, realistic reflections, avoid cluttered background.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset photo`

### Anime & Manga

Input: `画一个90年代动画风的图书馆少女`

Prompt: 1990s anime-style illustration of a cheerful teenage librarian character arranging books in a sunlit library, short chestnut hair, round glasses, blue cardigan, expressive eyes, clean ink linework, warm watercolor tones, soft afternoon window light, consistent character proportions, detailed shelves in the background.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset abstract --size 896x1200`

### Text in Image

Input: `产品横幅，文字 NEW ARRIVAL`

Prompt: Minimalist product banner with exact text "NEW ARRIVAL" centered at the top in bold clean sans-serif typography, matte white background, a single rose-colored skincare jar centered below the title, strong contrast, generous whitespace, professional ecommerce photography, avoid extra text overlays.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset text-poster`

### Concept Art

Input: `科幻城市概念图`

Prompt: Cinematic concept art of a futuristic coastal city built around a glowing vertical energy tower, small aircraft in the sky for scale, foreground observation deck with tiny silhouettes, layered bridges in the midground, ocean and storm clouds in the background, volumetric blue rim light, misty atmosphere, detailed production design, coherent spatial layout.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset concept`

### Abstract & Artistic

Input: `抽象海报，主题是时间流动`

Prompt: Abstract artistic poster about the flow of time, Bauhaus-inspired geometric composition, overlapping circles and diagonal lines suggesting motion, deep navy and warm amber palette with silver accents, flat screen-print texture, balanced negative space, clean modern gallery-poster finish, avoid cluttered background.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset abstract`

### Layout & Composition

Input: `左右对比图，过去和未来`

Prompt: Split-screen conceptual poster comparing past and future, left half shows an old analog clock and cracked stone texture, right half shows a clean glowing city skyline, vertical divider at the center, equal visual weight on both sides, strong left-right contrast, centered symmetry, title space at the top, balanced negative space, cinematic lighting.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset concept`

## Acceptance Examples

### 1. Coffee Poster

Input: `做一张咖啡海报`

Prompt: Create a warm modern coffee poster. Place a ceramic cup of latte in the center on a wooden table, with visible steam rising upward. Add the exact title "Fresh Coffee" at the top center in large cream-colored serif lettering, and add the smaller text "Start your morning right" along the bottom. Use a deep espresso and cream color palette, soft morning window light, shallow depth of field, clean margins, readable typography, and a premium cafe advertising style.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset text-poster --use-pe`

### 2. Exact English Sale Poster

Input: `生成海报，必须写 Spring Sale 50% OFF`

Prompt: Create a fresh spring retail sale poster. Use a bright white and soft green background with flowers around the edges and clean open space in the center. Show the exact text "Spring Sale 50% OFF" in large readable lettering at the center, with "Spring Sale" above "50% OFF". Use crisp typography, strong contrast, soft daylight, balanced margins, and a modern retail poster style.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset text-poster`

### 3. Bilingual Flowchart

Input: `一张中英文双语流程图，标题是 The Coffee Making Process`

Prompt: Create a clean bilingual coffee-making flowchart infographic. Put the exact title "The Coffee Making Process" at the top center. Arrange five steps left to right with simple icons and exact labels: "1. Grind / 研磨", "2. Heat Water / 烧水", "3. Brew / 冲煮", "4. Pour / 倒入", "5. Enjoy / 享用". Use a cream background, dark brown text, aligned arrows, consistent spacing, readable typography, high contrast, and clean vector-style illustrations.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset infographic`

### 4. Four-Panel Comic

Input: `四格漫画，一个机器人学会做饭`

Prompt: Create a four-panel comic in a 2x2 grid with clean borders and consistent character design. Panel 1: a small friendly silver robot opens a cookbook in a bright kitchen, speech bubble "I can learn this." Panel 2: the robot carefully chops vegetables with a focused expression, speech bubble "Step one: be careful." Panel 3: the robot stirs a soup pot while steam forms a heart shape, speech bubble "It smells good!" Panel 4: the robot serves a colorful meal to a smiling human friend, speech bubble "Dinner is ready." Keep the robot's body shape, face screen, colors, and apron consistent across all panels.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset comic`

### 5. Ecommerce Product Image

Input: `电商主图，白色无线耳机，突出降噪和长续航`

Prompt: Create a premium ecommerce hero image for white wireless earbuds. Place the earbuds and charging case in the center on a soft light-gray background, with glossy reflections and rim lighting. Add two small feature callouts around the product with exact text: "主动降噪" and "36小时续航". Use clean spacing, accurate product shape, realistic materials, sharp edges, subtle shadows, and a high-end technology advertising style.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset product`

### 6. App Launch Screen

Input: `APP启动页，名字是 MindGarden`

Prompt: Create a polished mobile app launch screen for a wellness app. Use a vertical 9:16 layout with a calm illustrated garden at dawn. Put the exact app name "MindGarden" centered in the upper third in clean rounded typography. Place a small leaf logo above the name and the tagline "Grow a calmer day" near the bottom. Use soft green, white, and warm sunlight, spacious composition, crisp UI-style text, and aligned mobile-screen proportions.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset ui`

### 7. Text-Dense Sign

Input: `做一张说明牌，标题 Safety Rules，内容三条：Wear goggles, Keep hands clear, Stop before cleaning`

Prompt: Create a front-facing safety instruction board with a white background and dark navy text. Put the exact title "Safety Rules" at the top in large bold lettering. Below it, show three numbered lines with exact text: "1. Wear goggles", "2. Keep hands clear", "3. Stop before cleaning". Use simple safety icons beside each line, strong contrast, consistent line spacing, and a clean industrial signage style.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset text-poster --size 1200x896`

### 8. Detailed Prompt Minimal Rewrite

Input: `A detailed fantasy city at sunset, floating bridges, blue roofs, orange sky, two airships, cinematic lighting, wide angle, no people, highly detailed`

Prompt: Create a wide-angle cinematic fantasy city at sunset. Show blue-roofed towers connected by floating bridges, with exactly two airships in the orange sky. Keep the city highly detailed, with warm rim lighting, atmospheric depth, no people, and a grand establishing-shot composition.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<prompt>" --preset concept --no-use-pe`

## Repair Examples

### Text Is Misspelled

Problem: the generated poster misspelled "Spring Sale 50% OFF".

Repair Prompt: Create a simple spring retail poster with only one visible text string: "Spring Sale 50% OFF". Place that exact text in the center, bold sans-serif, dark green letters on a plain white background, high contrast, large margins, no other text, avoid distorted letters.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<repair prompt>" --preset text-poster --seed 42`

### Comic Panels Bleed Together

Problem: a four-panel comic merged scenes or mixed dialogue.

Repair Prompt: Create a strict 2x2 four-panel comic grid with thick black borders and clear separation. Panel 1 only: robot reads cookbook, speech bubble "I can learn this." Panel 2 only: robot chops vegetables, speech bubble "Step one: be careful." Panel 3 only: robot stirs soup, speech bubble "It smells good!" Panel 4 only: robot serves dinner, speech bubble "Dinner is ready." Keep one consistent silver robot in every panel, avoid overlapping panels.

Command: `python3 {baseDir}/scripts/generate.py --prompt "<repair prompt>" --preset comic --seed 42`
