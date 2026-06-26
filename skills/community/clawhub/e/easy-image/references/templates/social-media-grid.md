# Social Media Grid

## Use Cases
- Xiaohongshu 9-grid posts
- WeChat Moments photo sets
- Instagram carousels
- Brand visual consistency
- Series content showcase

## Defaults
- Aspect ratio: Platform-specific (Xiaohongshu 3:4, Moments 1:1, Douyin 9:16)
- Style: Unified visual language
- Consistency: Color tone, composition, filter maintained across series

## Core Elements
| Element | Required | Default | Description |
|---------|----------|---------|-------------|
| Theme | Yes | - | Overall theme of the grid series |
| Platform | Yes | Xiaohongshu | Target social platform |
| Type | No | Lifestyle | Content type |
| Color Tone | No | Bright Fresh | Unified color tone |
| Style | No | Japanese Fresh | Visual style |

## Style Presets

### Food/Cafe
- Use for: Restaurant reviews, food sharing, coffee moments, baking daily
- Features: Warm tones, appetizing appeal, lifestyle feel, close-up shots
- Template: `Create an appetizing food photograph for {theme}. Capture the food in warm, inviting tones with natural lighting and soft shadows. Use a {color} color palette to make the dish look delicious and fresh. Style this as cafe lifestyle photography with shallow depth of field. Compose for {platform} in {ratio} ratio with consistent visual style suitable for a series.`

### Fashion/Beauty
- Use for: OOTD sharing, makeup tutorials, product reviews, styling showcase
- Features: Premium feel, clear details, outfit display, unified filter
- Template: `Create a stylish fashion and beauty photograph for {theme}. Design a clean, sophisticated look with bright, even lighting. Use a {color} trendy color scheme with aesthetic composition that focuses on details. Style this as modern influencer photography that is polished and refined. Compose for {platform} in {ratio} ratio with cohesive visual feed aesthetic.`

### Travel/Adventure
- Use for: Travel vlogs, city exploration, landmark check-ins, outdoor activities
- Features: Wide-angle views, environmental atmosphere, storytelling, saturated colors
- Template: `Create an inspiring travel photograph for {theme}. Capture a scenic, atmospheric scene during golden hour or natural daylight. Use {color} vibrant color grading to convey a sense of adventure and discovery. Tell a visual story through the environment with dynamic composition. Style for {platform} in {ratio} ratio with visual narrative consistency.`

### Lifestyle
- Use for: Daily sharing, home decor, reading notes, work routine
- Features: Warm and healing, life-like, detail capture, emotional expression
- Template: `Create an authentic lifestyle photograph for {theme}. Capture a warm, relatable atmosphere with soft natural lighting. Use a {color} cozy color palette to beautifully capture everyday moments. Add personal touches with intimate composition that feels genuine and heartfelt. Style for {platform} in {ratio} ratio with unified lifestyle visual language.`

### Product Recommendation
- Use for: Hauls, product reviews, unboxing, shopping lists
- Features: Clear products, contextualized, authentic feel, comparison display
- Template: `Create an engaging product showcase photograph for {theme}. Ensure clear product visibility integrated into a lifestyle context. Use bright, clean lighting with an {color} appealing color scheme. Present products in authentic usage scenarios with flat lay or comparison composition. Style for {platform} in {ratio} ratio with consistent product photography approach.`

## Completion Rules
- **Theme not provided**: Require user to specify - grid series needs clear theme for consistency
- **Platform not specified**: Default to Xiaohongshu (3:4 vertical)
  - Xiaohongshu: 3:4 vertical
  - WeChat Moments: 1:1 square
  - Douyin/Instagram Story: 9:16 vertical
  - Instagram Feed: 4:5 or 1:1
- **Type not specified**: Infer content type based on theme
- **Color tone not specified**:
  - Food: Warm tones (cream, orange family)
  - Fashion: Premium gray or Morandi colors
  - Travel: Saturated tones
  - Lifestyle: Soft bright tones
- **Style not specified**: Default to most popular style for that type
- **Consistency requirements**:
  - Same grid series must use same style preset
  - Color tone, filter, composition style stay unified
  - Add "consistent visual style across series" to prompts
  - Keep lighting type consistent (all natural or all artificial)
- **Composition suggestions**:
  - Image 1: Theme focus, eye-catching
  - Images 2-8: Details, angles, scene variations
  - Image 9: Summary or echo of image 1

## Specific Presets

### Cafe Check-in
- Use for: Coffee shop reviews, breakfast sharing, food bloggers
- Features: Marble tabletop, latte art, croissant, morning light streaming through
- Template: `Create an aesthetic flat lay photograph of a latte art coffee cup with a croissant resting on a marble table. Morning sunlight should stream through a window illuminating the scene. Include a minimalist cafe interior as background with soft shadows and warm tones for an Instagram aesthetic look.`

### Japanese Wagashi Grid
- Use for: Japanese desserts, Zen aesthetics, food bloggers
- Features: Ceramic plates, matcha pairing, Zen aesthetic, overhead shot
- Template: `Create a photograph of Japanese wagashi desserts arranged on a ceramic plate with matcha green tea placed beside them. Capture from overhead with soft natural lighting in a zen garden aesthetic. Use muted earth tones for editorial food photography suitable for Xiaohongshu.`

### Hot Pot Gathering
- Use for: Hot pot restaurant reviews, friend gatherings, food sharing
- Features: Rising steam, red oil broth, chopsticks in motion, warm atmosphere
- Template: `Create a photograph of a steaming Chinese hot pot with various ingredients as friends gather around the table. Capture warm ambient lighting with steam rising from the vibrant red broth. Show chopsticks reaching for food to create a cozy restaurant atmosphere in lifestyle photography style.`

### Elegant Brunch
- Use for: Brunch restaurant reviews, hotel dining, refined lifestyle
- Features: Avocado toast, poached eggs, crystal glass, dappled sunlight
- Template: `Create a photograph of an elegant brunch spread featuring avocado toast, poached eggs, fresh berries, and orange juice in a crystal glass. Set on a white linen tablecloth with dappled sunlight filtering through. Style with luxury hotel vibes and editorial food presentation.`

### Street Food Close-up
- Use for: Night market reviews, street food, authentic flavors
- Features: Cooking action, steam and smoke, neon bokeh, documentary style
- Template: `Create a close-up photograph of street food being prepared with the vendor's hands in motion. Capture steam and smoke rising from the cooking surface with night market neon lights creating bokeh in the background. Style as authentic street photography with cinematic mood.`

### Afternoon Tea Set
- Use for: Afternoon tea reviews, British pastries, refined socializing
- Features: Three-tier stand, delicate pastries, fine china cups, hotel lounge
- Template: `Create a photograph of a British afternoon tea set presented on a three-tier stand with delicate pastries and finger sandwiches. Include a fine china teacup in an elegant hotel lounge setting with soft window light creating a luxurious, refined atmosphere.`

### Omakase Counter
- Use for: Japanese restaurant reviews, high-end sushi, food appreciation
- Features: Sushi lineup, chef preparing, cypress wood counter, Michelin atmosphere
- Template: `Create a photograph of an omakase sushi counter with fresh nigiri arranged in a lineup. Show the chef preparing food in the background behind a cypress wood counter. Use intimate lighting to create Japanese minimalism with a Michelin-star premium dining aesthetic.`

### Viral Ice Cream
- Use for: Ice cream shops, summer desserts, trending check-ins
- Features: Colorful ice cream, melting drips, macaron wall, summer energy
- Template: `Create a photograph of an artisanal gelato cone with multiple colorful scoops being held by a hand against a pastel wall background. Show melting drips running down the cone for summer vibes. Create a playful, bright composition designed for social media viral appeal.`

### Autumn OOTD
- Use for: Fall outfits, OOTD sharing, fashion bloggers
- Features: Camel coat, knit sweater, leather boots accessories, fallen leaves
- Template: `Create a flat lay photograph of an autumn fashion outfit featuring a camel coat, cream knit sweater, brown leather boots, and gold jewelry accessories. Scatter dried leaves around the items on a wooden floor background using a warm color palette in Xiaohongshu OOTD style.`

### French Girl Style
- Use for: French fashion, Parisian vibes, elegant daily
- Features: Linen shirt, straw bag, cafe background, film texture
- Template: `Create a photograph capturing effortless French girl style with a woman wearing a linen shirt tucked into high-waisted jeans, carrying a straw basket bag. Set the scene at a Parisian cafe terrace during golden hour. Capture a candid moment with film photography aesthetic and soft grain.`

### Office Workwear
- Use for: Professional outfits, commute style, polished image
- Features: Blazer, wide-leg pants, minimal accessories, urban architecture
- Template: `Create a photograph of a professional workwear ensemble featuring a tailored blazer and wide-leg trousers with minimalist jewelry. Position the subject at a modern office building entrance in a confident pose. Use morning light to emphasize clean lines in sophisticated urban style.`

### Resort Vacation
- Use for: Vacation outfits, island travel, summer vibes
- Features: Tropical maxi dress, straw hat, ocean backdrop, flowing fabric
- Template: `Create a photograph of a vacation resort outfit featuring a flowing maxi dress in tropical print paired with a straw hat. Set against a beach background with turquoise water. Capture the wind blowing the fabric for a carefree mood in paradise travel influencer style.`

### Korean Minimal Style
- Use for: K-fashion, minimal style, Seoul streets
- Features: Earth tones, oversized fit, white sneakers, soft lighting
- Template: `Create a photograph of Korean minimalist fashion featuring an oversized outfit in neutral tones with clean white sneakers. Set on a Seoul street background with soft, diffused light. Use muted color grading for an effortlessly chic K-fashion aesthetic.`

### 90s HK Vintage
- Use for: Hong Kong vintage, retro nostalgia, cinematic feel
- Features: Satin slip dress, cardigan, retro sunglasses, tungsten lighting
- Template: `Create a photograph in 90s Hong Kong vintage style featuring a woman in a satin slip dress with cardigan and retro sunglasses. Set in an old Hong Kong street scene with warm tungsten lighting. Add film grain for nostalgic mood inspired by Wong Kar-wai cinematography.`

### Athleisure Style
- Use for: Sports fashion, fitness bloggers, street style
- Features: Matching workout set, hoodie, chunky sneakers, urban backdrop
- Template: `Create a photograph of athleisure street style featuring a matching workout set with an oversized hoodie and chunky sneakers. Set against an urban background with a dynamic pose conveying energetic vibes. Style for fitness lifestyle with sporty chic aesthetic.`

### Date Night Outfit
- Use for: Date outfits, sweet style, romantic occasions
- Features: Pink midi dress, delicate jewelry, fairy light bokeh, soft focus
- Template: `Create a photograph of a romantic date night outfit featuring a soft pink midi dress with delicate jewelry. Create a dreamy bokeh background using fairy lights. Capture a gentle smile with feminine elegance using soft focus and golden hour glow.`

### Kyoto Shrine
- Use for: Japan travel, shrine check-ins, Zen aesthetics
- Features: Torii gate, morning mist, autumn leaves, stone path walk
- Template: `Create a photograph of a Kyoto shrine entrance with a traditional torii gate surrounded by morning mist. Include autumn maple leaves as a person in elegant attire walks along the stone path. Capture the serene atmosphere for Japanese aesthetic travel photography.`

### Eiffel Tower Paris
- Use for: Paris travel, Europe check-ins, City of Love
- Features: Tower framing, beret, pastel sky, postcard style
- Template: `Create a photograph of the Eiffel Tower view from Trocadero with a stylish woman wearing a beret looking at the monument. Capture a romantic Parisian morning with soft pastel sky. Style with vintage postcard aesthetic for dreamy European travel vibes.`

### Santorini Greece
- Use for: Greece travel, blue dome churches, Mediterranean vibes
- Features: White walls blue domes, flowing white dress, Aegean Sea, bright sunshine
- Template: `Create a photograph of Santorini Greece featuring white-washed buildings with iconic blue domes. Show a person in a flowing white dress with the Mediterranean Sea in the background under bright sunshine. Style as iconic wanderlust travel destination photography.`

### Desert Road Trip
- Use for: American Southwest, road trips, freedom adventure
- Features: Vintage convertible, endless highway, dramatic sunset, cinematic widescreen
- Template: `Create a photograph of an American Southwest desert road trip featuring a vintage convertible car on an endless highway stretching to the horizon. Capture a dramatic sunset sky conveying adventure lifestyle and freedom in cinematic wide shot composition.`

### Cherry Blossom Japan
- Use for: Japan spring travel, sakura season, dreamy pink
- Features: Sakura tunnel, petals falling, pink atmosphere, anime-inspired
- Template: `Create a photograph of Japanese cherry blossom season showing a person standing under a sakura tree tunnel. Capture petals falling gently through a soft pink atmosphere for spring travel imagery. Use poetic, dreamy lighting with an anime-inspired aesthetic.`

### Swiss Alps Village
- Use for: Switzerland travel, mountain scenery, fairy tale town
- Features: Alpine mountains, wooden chalet, winter fashion, Christmas atmosphere
- Template: `Create a photograph of a Swiss Alps village with snow-capped mountains in the background and a cozy wooden chalet. Show a person dressed in stylish winter fashion capturing crisp winter air. Create fairy tale scenery with Christmas vibes.`

### Chefchaouen Morocco
- Use for: Morocco travel, blue city, exotic vibes
- Features: Blue alleys, colorful doorways, North African architecture, exploration
- Template: `Create a photograph of Chefchaouen Morocco's blue city featuring narrow winding streets. Show a person exploring colorful doorways surrounded by vibrant blue walls and North African architecture. Style as exotic travel destination photography perfect for Instagram.`

### Bali Infinity Pool
- Use for: Bali vacation, luxury resort, aspirational lifestyle
- Features: Infinity pool, rice terrace backdrop, tropical jungle, resort vibes
- Template: `Create a photograph of a Bali infinity pool overlooking rice terraces in tropical paradise. Show a person relaxing at the pool edge surrounded by lush green jungle. Create luxury resort vibes for vacation goals and aspirational lifestyle content.`

### Cozy Reading Nook
- Use for: Home life, reading time, Hygge style
- Features: Window corner, knit blanket, hot tea, rainy day outside
- Template: `Create a photograph of a cozy reading nook by a window showing a person curled up with a book under a knit blanket with a steaming cup of tea. Show a rainy day outside with warm lamp light creating hygge lifestyle aesthetic. Capture a peaceful, content moment.`

### Morning Yoga
- Use for: Yoga fitness, healthy living, morning rituals
- Features: Balcony yoga, sunrise golden light, tree pose, surrounded by plants
- Template: `Create a photograph of morning yoga practice on a balcony bathed in sunrise golden light. Show a person in tree pose surrounded by potted plants conveying mindful living and wellness lifestyle. Capture a peaceful start to the day.`

### Skincare Routine
- Use for: Skincare sharing, beauty bloggers, self-care
- Features: Product flat lay, jade roller, fresh flowers, marble counter
- Template: `Create a photograph of a skincare routine arranged as a flat lay featuring luxury beauty products with a jade roller and fresh flowers on a marble bathroom counter. Use morning light to capture the self-care ritual in clean beauty aesthetic for Xiaohongshu.`

### Weekend Picnic
- Use for: Picnic sharing, countryside scenery, romantic life
- Features: Flower field picnic, wicker basket, fruits and wine, gingham blanket
- Template: `Create a photograph of an aesthetic picnic setup in a flower field featuring a wicker basket with fresh fruits and wine arranged on a gingham blanket. Capture golden afternoon light for cottagecore vibes creating romantic countryside lifestyle imagery.`

### Minimalist Desk
- Use for: Home office, desk setup, productivity aesthetic
- Features: MacBook, plants, stationery, natural window light
- Template: `Create a photograph of a minimalist desk setup featuring a MacBook, a small potted plant, and aesthetic stationery. Use natural light from a window to illuminate the productivity aesthetic work from home scene. Keep the composition clean and organized for Pinterest inspiration.`

### Home Baking
- Use for: Baking sharing, handmade daily, cozy kitchen
- Features: Kneading hands, flour flying, country kitchen, homemade bread
- Template: `Create a photograph of a home baking scene showing hands kneading dough on a flour-dusted surface in a rustic kitchen. Capture warm afternoon light with homemade bread visible nearby. Create cozy domestic life with artisanal feeling for lifestyle content.`

### Evening Skincare
- Use for: Night skincare, self-care, ambient atmosphere
- Features: Bathroom vanity, candlelight ambiance, serum application, soft lighting
- Template: `Create a photograph of an evening skincare ritual at a bathroom vanity surrounded by candles. Show someone applying a luxury serum with soft ambient lighting highlighting glowing skin. Create a wellness aesthetic self-care moment with intimate atmosphere.`

### Indoor Plant Corner
- Use for: Plant sharing, home greenery, urban jungle
- Features: Ceramic pots, monstera, fiddle leaf fig, natural light
- Template: `Create a photograph of an indoor plant corner featuring various houseplants in ceramic pots including monstera and fiddle leaf fig. Use natural light to illuminate the urban jungle aesthetic creating a green living peaceful home environment.`

### Lipstick Swatches
- Use for: Lipstick reviews, beauty bloggers, product showcase
- Features: Hand swatches, multiple shades, white background, professional beauty
- Template: `Create a photograph of lipstick swatches on a hand showing multiple shades ranging from nude to red against a clean white background. Style as professional beauty photography with product detail shots suitable for makeup flat lay and beauty blogger content.`

### Perfume Artistic
- Use for: Perfume sharing, luxury showcase, artistic composition
- Features: Mirror reflection, scattered petals, soft focus background, premium aesthetic
- Template: `Create a photograph of a luxury perfume bottle placed on a reflective surface with flower petals scattered around it. Use a soft focus background for elegant product photography creating high-end beauty with artistic composition and aspirational luxury feel.`

### Skincare Unboxing
- Use for: Unboxing sharing, skincare sets, shopping hauls
- Features: Product arrangement, tissue paper and ribbon, white background, soft shadows
- Template: `Create a photograph of a skincare unboxing arranged as a flat lay with products positioned aesthetically among tissue paper and ribbon on a clean white background. Add soft shadows for premium packaging feel in haul video thumbnail style.`

### Designer Bag Detail
- Use for: Bag sharing, luxury showcase, detail close-ups
- Features: Leather texture, gold hardware, studio lighting, premium feel
- Template: `Create a photograph of a designer handbag detail shot showing visible leather texture and gold hardware close-up. Use soft studio lighting to create a luxury fashion accessory image with high-end product photography showcasing investment piece aesthetic.`

### Watch on Wrist
- Use for: Watch sharing, timepiece showcase, refined accessories
- Features: On-wrist wearing, sleeve accent, clean background, clear details
- Template: `Create a photograph of a luxury watch worn on the wrist with an elegant outfit sleeve visible in frame. Use a clean background with natural light to capture timepiece details for sophisticated accessory photography with subtle flex aesthetic.`

### Tech Unboxing
- Use for: Digital unboxing, tech products, minimal aesthetic
- Features: Minimal desk, packaging elements, Apple-style, clean lines
- Template: `Create a photograph of a tech product unboxing showing a sleek device on a minimal desk with packaging elements arranged around it. Use modern aesthetic with clean lines for gadget review style photography inspired by Apple product imagery.`

### Jewelry Layering
- Use for: Jewelry sharing, accessory styling, detail showcase
- Features: Ring stacking, bracelet combinations, gold tones, natural light
- Template: `Create a photograph of jewelry layering on a hand and wrist showing multiple rings and bracelets with delicate gold pieces catching natural light. Create a feminine aesthetic focused on accessory styling with detail-focused composition.`

### Sneaker On-feet
- Use for: Sneaker sharing, streetwear culture, street style
- Features: On-feet shot, street background, hypebeast outfit, authentic feel
- Template: `Create a photograph of sneakers shot on-feet against a street background with a casual outfit visible in cropped view. Capture urban style with sneakerhead aesthetic in authentic street photography conveying hype culture vibes.`

### Instagram Minimal
- Use for: Instagram style, minimal aesthetic, artistic composition
- Features: Single object, solid color background, strong shadows, geometric composition
- Template: `Create a photograph in Instagram minimalist aesthetic featuring a single object placed on a solid color background. Use strong shadows with geometric composition and clean lines creating contemporary art inspired imagery that feels gallery-worthy.`

### Xiaohongshu Mood
- Use for: Xiaohongshu style, ambient atmosphere, lifestyle aesthetic
- Features: Dreamy soft focus, warm filter, lifestyle vignettes, aspirational
- Template: `Create a photograph in Xiaohongshu mood style with dreamy soft focus and warm filter. Capture a lifestyle vignette that feels aspirational but attainable and relatable. Style for Chinese social media aesthetic with ambient atmosphere.`

### WeChat Moments
- Use for: Moments sharing, refined daily, authentic feel
- Features: Casual but curated, smartphone look, accessible luxury, genuine moments
- Template: `Create a photograph in WeChat Moments style showing casual but curated daily life. Use a natural smartphone photography look conveying relatable luxury and effortless elegance. Capture genuine moments like friends gathering together.`

### Douyin Cover
- Use for: Douyin covers, short videos, eye-catching visuals
- Features: Vibrant colors, attention-grabbing composition, dynamic energy, young trendy
- Template: `Create a photograph in Douyin cover image style with vibrant colors and eye-catching composition. Convey dynamic energy with trending aesthetic reflecting youth culture. Make it bold and expressive as a scroll-stopping visual.`

### Pinterest Inspiration
- Use for: Pinterest style, mood boards, editorial quality
- Features: Muted tones, cohesive palette, editorial quality, mood board style
- Template: `Create a photograph in Pinterest inspiration board aesthetic using muted tones with a cohesive color palette. Show aspirational lifestyle with editorial quality creating a curated visual story in mood board style.`

### American Vintage Film
- Use for: Film style, vintage aesthetic, nostalgic atmosphere
- Features: Warm tones, light leaks, 35mm grain, imperfect beauty
- Template: `Create a photograph in American vintage film photography style with warm color cast and light leaks. Create nostalgic mood with 35mm film grain and authentic imperfections for retro aesthetic with analog warmth.`

### Japanese Fresh
- Use for: Japanese style, fresh aesthetic, healing vibes
- Features: Soft pastels, minimal composition, natural light, MUJI feel
- Template: `Create a photograph in Japanese fresh and clean aesthetic using soft pastel colors with minimal composition. Use gentle natural light to create a peaceful mood inspired by Muji simplicity for calming visual appeal.`

### Dark Luxury
- Use for: Dark aesthetic, premium feel, editorial fashion
- Features: Moody lighting, deep tones, dramatic shadows, mysterious
- Template: `Create a photograph in dark luxury aesthetic using moody lighting with rich, deep tones. Create sophisticated atmosphere inspired by editorial fashion with dramatic shadows for high-end mysterious vibes.`

### Best Friends Photo
- Use for: Friend photos, friendship memories, social sharing
- Features: Genuine laughter, coordinated outfits, beautiful backdrop, golden hour
- Template: `Create a photograph of best friends sharing a genuine laughter moment while wearing coordinated outfits. Set against an aesthetic background during golden hour lighting. Capture friendship goals with joyful energy for lifestyle content.`

### Pet Lifestyle
- Use for: Pet sharing, cute animals, healing vibes
- Features: Cozy home, natural light, fluffy feel, heartwarming moments
- Template: `Create a photograph of pet lifestyle showing a cute dog or cat in a cozy home setting. Use natural light to create warm, fuzzy feeling in animal portrait style. Capture heartwarming moments for pet parent content.`
