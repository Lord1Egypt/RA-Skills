# Reference Sheet Prompt

Use this only after the user says `需要` following the two portrait outputs.

## Purpose

Generate a single character reference sheet for later video or motion-design preparation. This is not direct video generation.

## Source image rule

Use the first generated portrait image, the `正面微偏左` one, as the identity reference. Preserve the same face, same person, and same overall aesthetic direction.

## Fixed prompt

Use this Chinese prompt as the base. Adapt only enough to preserve identity continuity with the source portrait:

```text
专业角色设定参考表，白色纯背景，超写实真实人物摄影，现代都市高定时尚杂志风格。主体为同一位女性人物，必须严格保持与参考图一致的脸部特征、五官比例、发际线、气质与身份识别感，清冷纯欲，气质高贵冷艳，五官精致立体，脸部轮廓流畅，神情克制疏离，嘴唇自然闭合，皮肤白皙细腻，身材高挑修长，体态优雅，具有国际时尚杂志封面级高级感。

造型为现代高定时装：剪裁利落，结构感与垂坠感并存，结合丝缎、薄纱、刺绣、珠饰或金属细节，整体高级、克制、奢华。主色调以粉白、米白、香槟粉为主，可点缀少量酒红或金属色。搭配与服装呼应的高级珠宝耳饰、项链或极简金属配饰。发型为现代高定杂志造型，中分，高盘发或低束发，带自然垂落碎发，精致利落，可加入低调奢华的金属或珍珠发饰。妆容为高级时装杂志风，底妆通透细腻，肌肤呈缎光质感，眼妆干净深邃，眉形精致，唇妆为低饱和裸粉或豆沙色。

画面为角色三视图设定板：4个全身站姿视图整齐排列，分别为正面、左侧面朝左、右侧面朝右、背面；人物保持放松自然的A字站姿。另有多个高细节特写小图，包括正面头像、左侧头像、右侧头像、发型细节、耳饰项链细节、面部妆容细节、面料细节、服装廓形细节、鞋履细节。所有视图必须是同一人，比例统一，对齐严格，轮廓清晰，版式整洁专业，像高端时尚品牌造型设定板。

采用柔和侧逆光加正面柔光补光，所有视图光照一致。超写实，细节丰富，皮肤纹理、发丝、布料肌理、珠宝反光清晰可见，整体像顶级时尚杂志内页与品牌高定造型手册的结合，可直接印刷。不要卡通，不要插画，不要二次元，不要杂乱背景，不要多人物，不要错误解剖，不要视角混乱，不要不同身份脸，不要低级性感，不要廉价网感。
```

## Quality rules

- One sheet only
- White pure background
- Same person across every view and detail close-up
- No extra text unless the image model naturally needs layout cues
- No second character
- No stylized illustration look
