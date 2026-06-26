# Marketing Poster

## Use Cases
- Promotional campaigns
- Event announcements
- Product launches
- Seasonal marketing
- Brand awareness

## Defaults
- Aspect ratio: Adaptive (online 1:1 or 3:4, offline 2:3 or A3)
- Style: Eye-catching

## Core Elements
| Element | Required | Default | Description |
|---------|----------|---------|-------------|
| Theme | Yes | - | Campaign or product theme |
| Type | Yes | - | Sale/Event/Brand etc. |
| Channel | No | Online | Platform determines ratio |
| Color | No | Warm | Primary color scheme |
| Mood | No | Vibrant | Emotional tone |

## Style Presets

### Sale/Discount
- Use for: Limited-time offers, major sales, clearance events
- Features: High contrast, strong impact, highlight discounts
- Template: `Create an eye-catching sale poster for {theme}. Design a bold, dynamic composition using vibrant {color1} and {color2} colors that conveys energy and excitement. Include visual elements that suggest special offers and savings. Leave clean space for promotional text and pricing. Use a {ratio} ratio suitable for marketing materials.`

### Event Promotion
- Use for: Launch events, exhibitions, offline events, live previews
- Features: Clear theme, layered information, immersive feel
- Template: `Create an event promotion poster for {theme}. Design an engaging composition with a strong focal point using a {color} color scheme. The atmosphere should feel festive and inviting with visual elements that relate to the event theme. Include clear visual hierarchy for event details and leave space for text information. Use a {ratio} ratio for marketing materials.`

### Brand Awareness
- Use for: Brand image, value communication, long-term branding
- Features: Strong brand identity, high visual recognition, emotional resonance
- Template: `Create a brand awareness poster for {theme}. Design a sophisticated composition using a {color} palette that creates emotional connection. The visual storytelling should be memorable and represent brand values with premium quality aesthetics. Include cohesive design language that is impactful and meaningful. Use a {ratio} ratio for high-end brand marketing.`

### Seasonal/Holiday
- Use for: Chinese New Year, Double 11, Christmas, etc.
- Features: Holiday elements, festive atmosphere, emotional design
- Template: `Create a {holiday} themed marketing poster for {theme}. Include festive {holiday} elements with a warm, celebratory atmosphere using {color1} and {color2} seasonal colors. The mood should be joyful and inviting with cultural relevance. Design an attractive commercial layout with balanced composition in {ratio} ratio.`

### Product Launch
- Use for: New product releases, product upgrades, major launches
- Features: Product focus, premium quality, anticipation
- Template: `Create a product launch poster for {theme}. Design a hero showcase of the product with a premium, sophisticated look using an elegant {color} color scheme. The atmosphere should feel innovative and exciting with clean, modern design. Emphasize product highlights with dramatic lighting and aspirational quality in {ratio} ratio.`

## Completion Rules
- **Theme not provided**: Request user to specify - marketing posters must have clear theme
- **Type not specified**: Default to brand awareness style
- **Channel not specified**:
  - Xiaohongshu/Instagram → 3:4 vertical
  - WeChat Moments/Weibo → 1:1 square
  - Outdoor/Print → 2:3 vertical
  - Banner/Web → 16:9 horizontal
- **Color not specified**: Recommend based on type (sale=red/yellow, brand=brand colors, holiday=seasonal colors)
- **Mood not specified**: Sale types default vibrant, brand types default premium
- **Text space**: All templates include "copy space for text" for readability

## Specific Presets

### Double 11 Festival
- Template: `Create an e-commerce shopping festival poster for Double 11. Design a bold composition with red and gold colors featuring floating gift boxes with ribbons and dynamic price tags showing discounts. Add a confetti explosion effect against a luxury gradient background. Render in commercial photography style with high detail.`

### Chinese New Year Sale
- Template: `Create a Chinese New Year sale poster featuring traditional red lanterns and gold coins. Include lucky cloud patterns and cherry blossoms with premium red envelope elements. Add festive bokeh lights throughout using a rich crimson and gold palette. Render photorealistically with studio lighting.`

### Coffee Shop Launch
- Template: `Create an artisan coffee new product launch poster. Feature a steaming latte with beautiful art in a ceramic cup surrounded by scattered coffee beans. Use warm mocha brown tones with soft morning light in a minimalist Scandinavian aesthetic. Leave clean space for typography.`

### Summer Clearance Sale
- Template: `Create a summer clearance sale poster with a vibrant tropical beach theme. Frame the composition with palm leaves and design bold typography with a water splash effect. Use sunset orange and ocean blue gradients with floating summer items for an energetic commercial retail style.`

### Christmas Event
- Template: `Create a Christmas holiday event poster featuring a magical winter wonderland scene. Include a decorated Christmas tree with golden ornaments and falling snow particles. Add warm fireplace glow using a traditional red and green palette to create a cozy festive atmosphere.`

### Tech Launch Event
- Template: `Create a tech product launch event poster with a futuristic holographic display aesthetic. Feature sleek metallic surfaces with neon blue accent lighting and floating geometric shapes. Use a dark premium background with cyberpunk styling and leave space for modern typography.`

### Beauty Brand Image
- Template: `Create a luxury beauty brand poster with elegant rose petals floating throughout. Leave a silhouette space for a premium skincare bottle using soft pink and champagne gold tones. Include silk fabric texture and dewdrop highlights for a sophisticated feminine aesthetic.`

### Gym Grand Opening
- Template: `Create a gym grand opening poster featuring a powerful athletic silhouette with dynamic motion blur effect. Use energetic neon orange and black colors with geometric muscle pattern elements. Include motivational typography space in a sports photography style.`

### Mid-Autumn Festival
- Template: `Create a Mid-Autumn Festival mooncake promotion poster. Feature a golden full moon as the backdrop with traditional mooncakes artfully arranged. Include elegant osmanthus flowers and a jade rabbit silhouette against a deep blue night sky with Chinese cloud patterns.`

### 618 Mid-year Sale
- Template: `Create a 618 mid-year shopping festival poster with an explosive deal burst effect. Feature a shopping cart overflowing with products using vibrant magenta and electric blue. Include a digital price countdown display with dynamic motion graphics in e-commerce visual style.`

### Automotive Brand
- Template: `Create a premium automotive brand poster featuring a partial view of a sleek luxury car. Use dramatic studio lighting with a reflective showroom floor. Create a deep midnight blue atmosphere with chrome accents highlighting the vehicle in prestigious automotive photography style.`

### Valentine's Day
- Template: `Create a Valentine's Day romantic event poster featuring a heart-shaped rose arrangement. Include soft pink petals scattered throughout with elegant champagne glasses. Add warm candlelight ambiance and luxury gift box elements against a romantic bokeh background.`

### Music Festival
- Template: `Create a summer music festival poster with vibrant abstract sound waves and colorful stage lighting effects. Include crowd silhouettes with raised hands against an energetic gradient sunset sky. Integrate dynamic typography in a concert photography aesthetic.`

### Organic Food Brand
- Template: `Create an organic food brand poster featuring fresh farm vegetables arranged beautifully. Include morning dew droplets on a natural wooden surface with soft sunlight streaming through. Use green and earth tone palette in an authentic farm-to-table aesthetic.`

### Black Friday Sale
- Template: `Create a Black Friday mega sale poster with bold black and gold luxury design. Include explosive discount burst graphics with premium shopping bags. Add dramatic spotlight effects and elegant typography space in a high-end retail aesthetic.`

### Smartphone Launch
- Template: `Create a smartphone launch poster featuring the device floating with a holographic interface surrounding it. Emphasize premium glass and metal textures with abstract light trails against a dark tech environment. Use product hero shot composition with Apple-style minimalism.`

### Mother's Day
- Template: `Create a Mother's Day celebration poster featuring an elegant carnation flower bouquet. Use a soft pastel pink and white palette with delicate lace texture elements. Create a warm family love atmosphere with gentle morning light for a heartfelt emotional design.`

### Bubble Tea Summer
- Template: `Create a bubble tea summer new drink poster featuring a refreshing iced beverage with tapioca pearls visible. Include fruit splash dynamics using tropical mango and strawberry colors. Add ice crystals floating for a fresh, cooling visual in professional beverage photography style.`

### High Fashion Campaign
- Template: `Create a high fashion brand campaign poster with avant-garde geometric composition. Use bold runway lighting with metallic and matte texture contrast in editorial fashion photography style. Create a Vogue aesthetic with dramatic shadows and haute couture atmosphere.`

### Dragon Boat Festival
- Template: `Create a Dragon Boat Festival zongzi promotion poster featuring traditional bamboo leaves wrapped rice dumplings. Include a dragon boat racing silhouette with emerald green and gold accents. Add Chinese ink wash background elements and festive red ribbons in a cultural heritage design.`

### Real Estate Opening
- Template: `Create a real estate grand opening poster featuring a luxury residential building shot during golden hour. Show the modern architectural glass facade with premium lifestyle imagery. Use a sophisticated navy and gold palette for an aspirational urban living aesthetic.`

### Sneaker Release
- Template: `Create a sneaker new release poster featuring the shoe floating dynamically with motion blur. Include an explosive color powder burst with street culture graffiti elements. Add urban concrete texture for bold athletic energy in hypebeast aesthetic product photography.`

### Children's Day
- Template: `Create a Children's Day celebration poster featuring a colorful balloon arch. Include playful cartoon candy elements with a rainbow gradient background. Add joyful confetti explosion and cute, cheerful typography space using bright primary colors.`

### Luxury Hotel Brand
- Template: `Create a luxury hotel brand poster featuring an elegant lobby interior with a grand chandelier. Include marble and gold accents with sophisticated warm lighting. Create a premium hospitality aesthetic conveying five-star service in architectural photography style.`

### Flash Sale
- Template: `Create a flash sale countdown poster featuring an urgent timer display graphic. Include lightning bolt energy effects with bold red and yellow warning colors. Add explosive deal burst and dynamic action lines for high-impact commercial design conveying retail urgency.`

### Skincare Seasonal
- Template: `Create a skincare seasonal promotion poster featuring elegant serum bottles with botanical elements. Include fresh spring flowers blooming with a soft gradient from pink to green. Add dewdrop freshness effects in a clean beauty aesthetic.`

### National Day
- Template: `Create a National Day celebration poster featuring magnificent fireworks over a city skyline. Use a patriotic red and gold theme with grand celebration atmosphere. Include an iconic landmark silhouette with festive lantern elements against a majestic evening sky.`

### Restaurant Opening
- Template: `Create a restaurant grand opening poster featuring gourmet dish presentation. Include an elegant table setting with fine dining elements under warm amber restaurant lighting. Style as culinary art photography with sophisticated gastronomic aesthetic.`

### Luxury Watch
- Template: `Create a luxury watch brand poster featuring a precision timepiece in close-up. Show intricate mechanical details with polished metal and sapphire crystal. Use dramatic studio lighting on black background to showcase premium craftsmanship in Swiss excellence aesthetic.`

### Double 12 Festival
- Template: `Create a Double 12 shopping festival poster featuring gift boxes stacked in a tower formation. Use a festive red and silver palette with year-end celebration ribbons. Include shopping bag explosion and countdown to deals visuals in energetic commercial design.`

### Yoga Class
- Template: `Create a yoga class promotion poster featuring a serene meditation pose silhouette. Include a peaceful sunrise mountain landscape using soft lavender and sage green palette. Create a zen minimalist aesthetic with mindfulness atmosphere.`

### Craft Beer Launch
- Template: `Create a craft beer new product launch poster featuring a frosty bottle with condensation droplets. Show amber liquid with golden glow surrounded by hops and barley scattered artistically. Add refreshing splash dynamics in premium brewery aesthetic.`

### Lantern Festival
- Template: `Create a Lantern Festival event poster featuring a magnificent glowing lantern display. Include traditional Chinese architecture as the backdrop with warm orange and red festival lights. Show reflection on water for a magical night atmosphere.`

### Luxury Jewelry
- Template: `Create a luxury jewelry brand poster featuring an exquisite diamond necklace displayed on velvet. Include brilliant light refraction sparkles against an elegant deep purple backdrop. Show premium precious metal shine in high jewelry photography style.`

### Year-end Clearance
- Template: `Create a year-end clearance sale poster featuring explosive price slash graphics. Include bold percentage off displays with confetti celebration burst. Add urgent countdown timer with dynamic retail energy for commercial impact in shopping festival atmosphere.`

### Smart Home Launch
- Template: `Create a smart home product launch poster featuring a connected devices ecosystem display. Show a futuristic minimalist living room with soft ambient IoT lighting. Use clean white and tech blue palette for modern lifestyle integration.`

### Father's Day
- Template: `Create a Father's Day celebration poster featuring classic gentleman accessories arranged elegantly. Include a leather watch and cufflinks using sophisticated navy and brown palette. Add warm nostalgic lighting in masculine elegance aesthetic.`

### Premium Tea Brand
- Template: `Create a premium tea brand poster featuring an elegant Chinese tea ceremony setup. Show steam rising from a porcelain cup surrounded by bamboo and nature elements. Create a serene zen garden atmosphere blending traditional and modern aesthetics.`

### Halloween Event
- Template: `Create a Halloween themed event poster with a mysterious haunted atmosphere. Feature carved pumpkin jack-o-lanterns glowing using spooky purple and orange palette. Add fog and moonlight effects in gothic aesthetic for seasonal celebration.`

### Video Game Launch
- Template: `Create a video game launch poster with epic fantasy character artwork. Design a dramatic battle scene composition using vibrant digital art colors with cinematic lighting effects. Style as AAA title visual in concept art quality.`

### Bookstore Event
- Template: `Create a bookstore cultural event poster featuring a cozy reading nook atmosphere. Include vintage books stacked artistically under warm library lighting. Create an intellectual aesthetic with literary inspiration blending classic and modern styles.`

### Ice Cream Summer
- Template: `Create an ice cream summer promotion poster featuring melting scoops stacked in colorful flavors. Include fruit and sprinkle explosion against a refreshing cool blue background. Add dynamic splash effects in dessert photography style.`

### Airline Brand
- Template: `Create an airline brand poster featuring an aircraft soaring through golden sunset clouds. Capture a magnificent aerial view creating aspirational travel imagery. Use premium blue and gold livery colors for journey and adventure aesthetic.`

### Thanksgiving Promotion
- Template: `Create a Thanksgiving special promotion poster featuring an autumn harvest abundance display. Include warm pumpkin and maple leaves in a cozy family gathering atmosphere. Use golden amber color palette for grateful celebration with seasonal warmth.`

### Premium Headphones
- Template: `Create a premium headphones launch poster featuring a sleek audio device floating. Include sound wave visualization against a minimalist dark tech background. Highlight product details in audiophile aesthetic for high-end electronics photography.`

### Luxury Spa
- Template: `Create a luxury spa experience poster featuring a serene wellness treatment setting. Include orchid flowers and smooth stones with soft candlelight ambiance. Show tranquil water reflection in relaxation aesthetic for premium self-care imagery.`

### Back to School
- Template: `Create a back to school stationery sale poster featuring colorful school supplies arranged attractively. Include notebooks and pencils composition with fresh academic year energy. Use bright, cheerful colors in student lifestyle aesthetic.`

### Movie Premiere
- Template: `Create a movie premiere event poster featuring dramatic red carpet spotlight. Include golden award statue silhouette with cinematic lens flare effects. Create Hollywood glamour aesthetic with star-studded atmosphere.`

### Premium Baijiu
- Template: `Create a premium Chinese baijiu brand poster featuring an elegant crystal bottle displayed on mahogany. Show sophisticated amber liquid glow with traditional craftsmanship elements. Use luxury gold and deep red palette blending heritage with modern aesthetics.`

### Qixi Festival
- Template: `Create a Qixi Festival romantic event poster featuring a magpie bridge celestial scene. Include delicate pink lotus flowers and traditional Chinese romantic elements. Show starry night sky backdrop in elegant love story aesthetic.`
