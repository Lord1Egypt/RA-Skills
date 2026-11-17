# Prompts Reference — AI Concept Art for Figures

Load this file when generating figure concept images or moving from image to a printable model.

State the boundary up front in any answer: **AI accelerates T1 and nothing else.** It cannot do T2 to any usable degree.

## 1. Capability Boundary by Stage

| Stage | Can | Cannot | Status |
|---|---|---|---|
| T0 | competitor scanning, reference gathering | deciding whether the product should exist | assist only |
| T1 | 30 concepts, front/side views, color variants, material try-outs | consistency across angles, center-of-gravity judgment, manufacturability | **major speedup** |
| T2 | image-to-3D rough block-out | splitting, draft, wall, tolerance — all manual | effectively unusable |
| T3 | packaging visuals, promo renders | true painted appearance, product photography | partial |

## 2. Seven-Segment Prompt Skeleton

Fill all seven. Skipping segment six is the most common reason output looks like an illustration instead of a product.

| Segment | Content | Example fragments |
|---|---|---|
| ① Category anchor | what the object *is* | 盲盒手办 / 1:7 商业化手办 / 3dtoy / 手办钥匙扣 |
| ② Style anchor | locks the rendering style | moonlab_studio 风格 / 泡泡玛特风格 / 粗线条描边 / 涂鸦 / 极简 |
| ③ Subject | character, costume, props, material | 荧光粉金属外骨骼，液压关节带齿轮细节，胡萝卜造型火箭筒 |
| ④ Proportion | controls chibi-ness | 头身比 8:2，头大身体小 / 头身比 1:1.5 |
| ⑤ Color ratio | prevents color chaos | 主色土黄 60% + 暗红 25% + 浅蓝 15% |
| ⑥ Process evidence | makes it read as a photographed product | 透明亚克力圆形底座、背后包装盒印原画、屏幕显示 ZBrush 建模界面、PVC 材质清晰体现 |
| ⑦ Quality suffix | raises detail density | 8K、超级细节、oc 渲染、c4d、杰作、质量最好 |

### Reusable template

```
【品类锚】+【风格锚】+【主体：角色/服饰/道具/材质】+【头身比】+【姿态动作】
+【主色 60% + 辅色 25% + 点缀 15%】+【背景约束】
+【工艺证据：底座/包装/材质】+【画质后缀】
```

### Worked examples

```
盲盒手办，机甲兔耳少女，荧光粉金属外骨骼，液压关节带齿轮细节，胡萝卜造型火箭筒，
战斗破损涂装，干净背景，8k，超级细节
```

```
Q版手办，moonlab_studio风格，面部：圆润鹅蛋脸，双眼清澈明亮（占比面部25%），眉毛细长，
鼻梁挺直，唇色粉嫩，耳朵小巧。僧袍：方形叠加，土黄与暗红相间。九环锡杖：金色曲线杖体，
顶端九个圆环，环处蓝色光效。动作：双手合十，站在莲花底座上。主色土黄60%+暗红25%+浅蓝15%，
背景纯白，用三根弧线象征寺院飞檐，8K材质
```

```
绘制图中角色的1/7比例商业化手办，写实风格，真实环境，背景有手办包装盒与电脑桌面场景，
后方电脑显示3D建模软件界面，呈现对应人偶的设计稿。使用透明亚克力圆形底座，底座上无文字，
屏幕内容为该手办的ZBrush建模过程，屏幕旁放着印有原画的玩具包装盒
```

## 3. Image → Printable Model Chain

1. **Front view** by text-to-image, then re-run with `side view` / `back view` added to the same prompt. Keep the style anchor identical; consistency comes from the anchor plus a first-image reference.
2. **Block out in Blender or ZBrush.** Do not ship a raw image-to-3D result — topology will be unusable.
3. **ZBrush:** Dynamesh to establish mass → TrimDynamic and Polish for hard edges → ZRemesher with Project to keep detail → subdivide to level 4.
4. **Split parts** per T2 stage one. Add pegs with 0.25–0.3 mm clearance and an anti-rotation key.
5. **Thicken and repair** (Netfabb or similar). Hollow resin parts to 1.5–2 mm and add drain holes at the lowest point.
6. **Print → sand → filler → grey primer.** This step exposes everything the AI render hid.

Reference points that recur in working tutorials: keep each printed part a single watertight shell (merge SubTools or use Live Boolean, then verify no internal faces); orient parts so supports never land on the face; cure and clean before removing supports where possible; FDM minimum wall 1–1.5 mm, resin hollow 1.5–2 mm.

## 4. Three Hard Boundaries

1. **AI output cannot enter tooling.** It must be retopologized, thickened, and drilled. A beautiful render with a 0.4 mm arm is a scrapped part.
2. **AI generates suspended geometry, paper-thin limbs, and undercuts that cannot demold.** Every one of these is a reject at G2.
3. **Style anchors are a lever and a trap.** Once `moonlab_studio + 粗线条描边 + 纯色背景 + 8K` is used by ten thousand people, outputs converge. It gets you to "acceptable" fast and to "distinctive" almost never.

## 5. Review Checklist for AI Output

- [ ] Could this silhouette survive being filled black?
- [ ] Are there floating or unsupported elements?
- [ ] Is any limb thinner than 1 mm at the intended scale?
- [ ] Can the pose be split into 6–12 parts along natural seams?
- [ ] Does the base provide enough contact area for the center of gravity?
- [ ] Is the color count ≤4 after conversion to production colors?
