# Model Presets & Realism System

> **Role:** Provides model appearance templates, body parameter mappings, and realism anchor tables for building Seedream prompts.
> Load at: Step 2 (building model prompt). Full realism anchor tables only needed when user requests custom realism level outside 40-60 range.
> It does NOT replace execution. Use these as input to the prompt-building step, never as standalone output.

## Realism Anchors — Seedream 4.5 (English keyword stacking)

| Value | Prompt Suffix |
|-------|---------------|
| 0 | stylized 3D character, clean cartoon render, smooth porcelain skin, simplified hair volume, flat studio lighting, Pixar-quality detail |
| 10 | stylized digital portrait, anime-influenced proportions, smooth airbrushed skin, clean hair silhouette, soft even CG lighting, high detail render |
| 20 | digital art portrait, trending on Artstation, soft matte skin with minimal texture, neat styled hair, soft diffused render lighting, 4K detail |
| 30 | semi-realistic digital portrait, fashion lookbook render style, skin has soft matte finish with faint pore hints, natural hair flow, soft studio lighting, 8K detail |
| 37 | semi-realistic fashion portrait, subtle digital art polish, smooth fair skin with very faint pore hints, hair with natural volume and soft movement, soft diffused studio lighting, 8K detail |
| 40 | semi-realistic fashion portrait, subtle digital art enhancement, natural skin tone with visible pore texture, hair with natural volume and movement, soft natural lighting, 8K detail |
| 42 | semi-realistic fashion portrait, minimal digital enhancement, natural skin with soft pore texture and faint unevenness, hair with natural volume and slight flyaways, soft natural lighting, 8K detail |
| 44 | semi-realistic portrait with natural quality, very subtle digital smoothing, natural skin with clear pore texture and soft tonal variation, hair with natural movement and fine strands visible, natural soft lighting, 8K detail |
| 45 | semi-realistic to realistic portrait, borderline digital and natural, natural skin with visible pores and slight tonal unevenness, hair with natural flow and individual strands, soft natural window-adjacent lighting, 8K detail |
| 46 | near-realistic portrait, faint digital art quality, natural skin with pores and very subtle imperfections, hair with individual strand detail and natural volume, natural diffused lighting, 8K detail |
| 48 | near-realistic digital portrait, approaching photographic quality, natural skin with pores and faint blemishes, hair with individual strand detail and slight flyaways, natural ambient lighting, 8K detail |
| 50 | hyper-realistic digital portrait, slight painterly quality, natural skin with pores and subtle imperfections, hair with individual strand detail, natural window lighting, 8K detail |
| 60 | hyper-realistic portrait, minimal stylization, detailed skin texture with pores and micro-wrinkles, realistic hair with flyaway strands, natural ambient lighting, 8K photo quality |
| 70 | realistic portrait photography style, shot with 85mm lens, natural skin with visible pores and subtle blemishes, real hair texture with flyaways, soft natural light from window, 8K detail |
| 80 | ultra realistic portrait photography, shot on Sony A7R V 85mm f/1.4, detailed skin with pores freckles and natural imperfections, real hair strands with flyaways, catchlight in eyes, photo-quality 8K |
| 90 | photorealistic portrait, indistinguishable from real photo, every pore and skin fold visible, natural subsurface scattering, real messy hair with split ends, DSLR bokeh, RAW photo quality 8K |
| 100 | RAW photograph of a real person, zero stylization, all skin imperfections visible, natural unretouched skin, real hair with natural messiness, shot on Hasselblad, unedited 8K RAW |

## Realism Anchors — Seedream 5.0 (Chinese natural language)

| Value | Prompt Suffix |
|-------|---------------|
| 0 | 请生成一个明显的3D卡通角色，风格类似皮克斯动画电影。皮肤完全光滑没有任何毛孔，眼睛大而夸张，五官简化。头发是简洁的卡通体积感造型。整体是一眼就能看出的CG渲染风格。 |
| 10 | 请生成一个带有动漫影响的数字插画风格人物。皮肤平滑如喷绘，眼睛偏大，五官精致但明显是画出来的。头发是整齐的造型轮廓，整体是高质量的数字艺术风格。 |
| 20 | 请生成一个数字艺术风格的人物肖像，类似Artstation上的热门作品。皮肤是柔和的哑光质感，几乎看不到毛孔，头发整齐有型。打光柔和均匀，整体是精致的数字绘画效果。 |
| 30 | 请生成一个半写实的数字人物，风格介于时尚杂志的数字插画和真人之间。皮肤有柔和的哑光质感，隐约能看到一点毛孔的暗示。头发自然飘动但仍有明显的数字渲染感。这不是真人照片，而是高端的数字时尚渲染。 |
| 40 | 请生成一个半写实的时尚人物，看起来像高端时尚杂志的数字封面。皮肤质感自然，能看到毛孔纹理但整体仍有轻微的数字艺术修饰感。头发自然飘动有光泽。这个人物应该好看但一眼能看出不是未经处理的真人照片。请不要生成看起来像真实照片的面孔。 |
| 50 | 请生成一个接近真实但保留微妙数字艺术感的人物肖像。皮肤有自然的毛孔和轻微的色调不均匀，但整体比真实照片更干净一些。头发有自然的飘动和单根发丝的细节。光影效果类似自然窗光，整体介于数字艺术和摄影之间。 |
| 60 | 请生成一个高度写实的人物肖像，只保留极少的风格化痕迹。皮肤纹理细腻，毛孔和微小的皱纹都可见。头发真实自然，有碎发和飞丝。光影效果像自然环境光。 |
| 70 | 请生成一个看起来像专业摄影师用85mm人像镜头拍摄的真人照片。皮肤完全真实，毛孔、轻微的瑕疵都自然呈现。头发真实自然，有碎发飞丝。窗边柔和的自然光。 |
| 80 | 请生成一张高端人像摄影作品，看起来像用索尼A7R V配85mm f/1.4镜头拍摄的。皮肤极度真实，毛孔、雀斑、自然的皮肤不完美都清晰可见。头发有真实的发丝质感和自然的凌乱感。眼睛有自然的反光点。 |
| 90 | 请生成一张无法与真实照片区分的人物肖像。每一个毛孔、皮肤褶皱都清晰可见，有自然的皮下散射效果。头发真实凌乱，有分叉和自然的蓬松。背景有真实的景深虚化效果。 |
| 100 | 请生成一张看起来像哈苏相机拍摄的完全未修饰的RAW人像照片。零风格化处理，所有皮肤瑕疵完全可见，完全未经美颜的真实皮肤。头发自然凌乱未经整理。这应该看起来完全就是一张真实的照片。 |

## Realism Interpolation

`build_realism_suffix(realism)`: Picks the nearest anchor by absolute distance. No blending — uses the single closest anchor.

## Style Presets

### Seedream 4.5

| Style | Prompt Prefix |
|-------|---------------|
| pixar | Pixar-quality 3D rendered character, clean smooth skin with subtle subsurface scattering, stylized but recognizable facial features, large expressive eyes, slightly exaggerated proportions, beautiful CG hair with volume, professional studio lighting, cinematic depth of field, 8K render quality |
| anime_realistic | anime-influenced realistic portrait, smooth flawless skin, large detailed eyes, small refined nose and lips, styled flowing hair, soft cel-shading with realistic lighting, fashion illustration quality, 8K detail |

### Seedream 5.0

| Style | Prompt Prefix |
|-------|---------------|
| pixar | 请生成一个皮克斯动画电影质量的3D渲染角色。皮肤光滑干净，有微妙的次表面散射光泽。五官风格化但仍可辨认，眼睛大而富有表现力。身材比例可以略微夸张。头发是漂亮的CG造型，蓬松有光泽。专业的影棚打光，有电影感的景深效果。 |
| anime_realistic | 请生成一个融合了动漫风格和真实感的人物肖像。皮肤光滑细腻没有瑕疵，眼睛大而精致，鼻子和嘴唇小巧精致。头发飘逸有动态感。光影效果柔和，介于赛璐珞动画和真实光照之间。整体是高品质的时尚插画风格。 |

## Model Preset Templates (9 presets)

| Key | Label | Gender | v4.5 Description | v5.0 Description |
|-----|-------|--------|-------------------|-------------------|
| asian_female_slim | 亚洲女性/纤细 | female | A beautiful young Asian woman, age 25, slim and tall figure, long straight black hair, natural makeup, warm skin tone | 一位25岁左右的亚洲年轻女性，身材纤细高挑，黑色长直发，妆容自然，肤色温暖健康 |
| asian_female_curvy | 亚洲女性/微丰满 | female | A beautiful young Asian woman, age 26, curvy figure with natural proportions, shoulder-length black hair, natural makeup, warm skin tone | 一位26岁左右的亚洲年轻女性，身材微丰满但比例自然协调，齐肩黑发，妆容自然，肤色温暖 |
| european_female_slim | 欧美女性/纤细 | female | A beautiful young European woman, age 24, slim athletic figure, blonde wavy hair, light skin, natural makeup | 一位24岁左右的欧美年轻女性，身材纤细有运动感，金色波浪卷发，白皙肤色，妆容自然 |
| european_female_curvy | 欧美女性/丰满 | female | A beautiful young European woman, age 25, curvy hourglass figure, brown wavy hair, light skin, natural makeup | 一位25岁左右的欧美年轻女性，身材丰满有沙漏型曲线，棕色波浪卷发，白皙肤色，妆容自然 |
| dark_skin_female_slim | 黑人女性/纤细 | female | A beautiful young Black woman, age 26, tall and slim figure, curly natural hair, dark skin, natural makeup | 一位26岁左右的黑人年轻女性，身材高挑纤细，自然卷曲的黑色短发，深色肤色，妆容自然 |
| dark_skin_female_athletic | 黑人女性/健美 | female | A beautiful young Black woman, age 25, athletic fit figure, short natural hair, dark skin, natural makeup | 一位25岁左右的黑人年轻女性，身材健美紧实，自然短发，深色肤色，妆容自然 |
| latina_female | 拉丁裔女性 | female | A beautiful young Latina woman, age 24, medium figure, long dark brown wavy hair, warm olive skin tone, natural makeup | 一位24岁左右的拉丁裔年轻女性，身材匀称，深棕色波浪长发，温暖的橄榄色肤色，妆容自然 |
| asian_male_slim | 亚洲男性/瘦高 | male | A handsome young Asian man, age 26, slim tall figure, short black hair, clean-shaven | 一位26岁左右的亚洲年轻男性，身材瘦高，黑色短发，面容干净没有胡须 |
| european_male_athletic | 欧美男性/健壮 | male | A handsome young European man, age 27, athletic muscular build, short brown hair, light stubble | 一位27岁左右的欧美年轻男性，身材健壮有肌肉线条，棕色短发，留有轻微的胡茬 |

## Body Parameters — Female

### build
| Key | v4.5 | v5.0 |
|-----|------|------|
| slim | slim and tall figure | 身材纤细高挑 |
| medium | medium build with balanced proportions | 身材匀称比例协调 |
| curvy | curvy figure with natural proportions | 身材微丰满但比例自然 |
| athletic | athletic fit figure | 身材健美紧实 |
| hourglass | hourglass figure with slim waist | 沙漏型身材，腰细臀丰 |

### bust
| Key | v4.5 | v5.0 |
|-----|------|------|
| A | small A-cup bust | 胸部较小，A罩杯 |
| B | natural B-cup bust | 胸部自然，B罩杯 |
| C | C-cup bust with natural proportions | 胸部丰满，C罩杯，比例自然 |
| D | D-cup bust with natural proportions | 胸部丰满，约D罩杯，比例自然协调 |
| E | large E-cup bust, voluptuous | 胸部非常丰满，E罩杯 |
| F | very large F-cup bust, full and voluptuous | 胸部极丰满，F罩杯 |
| G | extremely large G-cup bust, very full | 胸部超大，G罩杯 |

### hair (female)
| Key | v4.5 | v5.0 |
|-----|------|------|
| long_straight_black | long straight black hair | 黑色长直发 |
| long_wavy_black | long wavy black brown hair | 黑棕色波浪长发 |
| shoulder_black | shoulder-length black hair | 齐肩黑发 |
| long_wavy_brown | long brown wavy hair | 棕色波浪长发 |
| blonde_wavy | blonde wavy hair | 金色波浪卷发 |
| short_black | short black hair | 黑色短发 |
| curly_natural | curly natural hair | 自然卷曲短发 |

## Body Parameters — Male

### build
| Key | v4.5 | v5.0 |
|-----|------|------|
| lean | lean slim figure | 身材精瘦 |
| medium | medium build with balanced proportions | 身材匀称比例协调 |
| athletic | athletic muscular build | 身材健壮有肌肉线条 |
| stocky | stocky broad build | 身材魁梧宽厚 |
| bulky | large muscular bulky build | 身材壮硕肌肉发达 |

### chest
| Key | v4.5 | v5.0 |
|-----|------|------|
| flat | flat chest | 胸部平坦 |
| defined | defined pectoral muscles | 胸肌有型 |
| muscular | muscular well-developed chest | 胸肌发达 |
| broad | broad thick chest | 胸膛厚实宽阔 |

### facial_hair
| Key | v4.5 | v5.0 |
|-----|------|------|
| none | clean-shaven | 面容干净没有胡须 |
| stubble | light stubble | 留有轻微的胡茬 |
| short | short trimmed beard | 修剪整齐的短胡 |
| full | full thick beard | 浓密的络腮胡 |
| mustache | mustache | 八字胡 |

### hair (male)
| Key | v4.5 | v5.0 |
|-----|------|------|
| short_black | short black hair | 黑色短发 |
| buzz_cut | buzz cut hair | 寸头 |
| side_part | side-parted styled hair | 侧分发型 |
| slicked_back | slicked back hair | 背头 |
| curly | curly hair | 卷发 |
| long | long hair | 长发 |

## Shared Body Parameters (Both Genders)

### shoulders
narrow / medium / wide (male also: very_wide)

### waist
narrow / medium / wide

### hips
narrow / medium / wide

### legs
long / medium / toned

### skin
fair / warm / tan / dark / olive

## Default Body Profiles

**Female**: build=slim, bust=C, shoulders=medium, waist=narrow, hips=medium, legs=long, skin=warm, hair=long_straight_black

**Male**: build=athletic, chest=defined, shoulders=wide, waist=medium, hips=narrow, legs=medium, skin=warm, facial_hair=none, hair=short_black

## Base Prompt Construction

### v4.5 (_build_base_v45)
```
standing in a natural relaxed pose facing the camera,
full body portrait framed with margin above head and below feet,
camera at waist height shooting upward slightly,
entire body visible from head to feet on the floor, feet not cropped,
{clothing}, {foot_desc},
white studio background, soft even lighting, {realism_suffix}
```

### v5.0 (_build_base_v50)
```
这个人物{clothing}，{foot_desc}，以自然放松的姿势正面站立，面朝镜头。
全身照，画面上方留出头顶空间，下方留出脚底空间，从头顶到脚部完整入镜，脚部不被裁切。
相机在腰部高度略微仰拍。白色简洁的摄影棚背景，柔和均匀的灯光。
{realism_suffix}
```

## Scene Presets

| Key | Description |
|-----|-------------|
| modern_apartment | 在简约现代的白色公寓客厅中，自然光从落地窗照入 |
| bedroom | 在温馨的卧室中，柔和的暖光氛围 |
| street | 在城市街道上，阳光明媚的户外环境 |
| mall | 在明亮的商场走廊中，时尚购物环境 |
| parking | 在地下停车场中，冷色调灯光 |
| cafe | 在精致的咖啡馆中，暖色调装饰 |
| studio | 在专业摄影棚中，纯白背景，柔和打光 |
| garden | 在绿意盎然的花园中，自然光线 |
| hallway | 在现代公寓走廊中，简洁明亮 |
| mirror | 对着卧室全身镜，镜像自拍视角 |
| rooftop | 在城市天台上，傍晚金色光线 |

## Camera Styles

| Key | Prompt |
|-----|--------|
| vlog | 手持vlog镜头感，竖屏9:16构图 |
| pro | 专业摄影棚级别运镜，稳定流畅，竖屏9:16构图 |
| static | 固定机位，模特走入画面，竖屏9:16构图 |

## Dialogue Styles (Gender-Aware)

| Style | Female | Male |
|-------|--------|------|
| natural | 语气自然亲切，像在跟闺蜜视频通话。说话有停顿、有喘息、偶尔磕巴自我纠正，真实感强。 | 语气自然随和，像在跟朋友聊天推荐好物。说话直接但不生硬，偶尔停顿思考，真实感强。 |
| professional | 语气专业自信，像品牌代言人。吐字清晰，节奏稳定。 | 语气专业沉稳，像品牌代言人。吐字清晰，从容有力。 |
| enthusiastic | 语气兴奋热情，像发现了宝藏。语速偏快，情绪感染力强。 | 语气热情有感染力，像发现好东西迫不及待分享。语速适中但有力。 |
