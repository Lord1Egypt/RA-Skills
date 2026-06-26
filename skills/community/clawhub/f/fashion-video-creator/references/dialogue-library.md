# Dialogue Library — Complete Reference

> This file provides raw dialogue materials for Seedance prompt assembly.
> Role: assist prompt composition by supplying garment-specific scripts.
> It does NOT replace the assembly workflow. Never output these dialogues directly — always compose through the workflow in SKILL.md.

## Dialogue Composition Formula

```
Full dialogue = OPENING + DIALOGUE_CORE + SELLING_CLOSING
```

Target audience auto-resolution:
- dress/bikini -> female audience
- All others -> same as model gender
- Can be overridden by user

---

## 1. Openings — by (model_gender, target_audience)

| (Gender, Audience) | zh | en |
|---------------------|----|----|
| (female, female) | 姐妹们你们快看... | Oh my god you guys need to see this... |
| (female, male) | 男生们看过来...这件我帮你们试了， | Hey guys, I tried this on for you, |
| (male, female) | 姐妹们，男生视角说一句... | Ladies, honest take from a guy... |
| (male, male) | 兄弟们，这件不吹不黑... | Bros, no BS on this one... |

---

## 2. Dialogue Core — 7 garment types x 2 genders x 2 languages

Female tone: expressive, filler words (嗯/就是/哇), emotional reactions.
Male tone: direct, fewer fillers, factual, confident.

### dress / female / zh
> 哇，不是，我真的没想到这条裙子上身效果这么好。你看这个面料，是那种...嗯...醋酸缎面的...（右手轻轻拉起裙摆展示）滑滑的凉凉的，而且有一定的厚度，不是那种廉价的薄纱感。然后你看这个车线...（右手翻开裙子内侧给镜头看）全部是包边走线的，没有毛边，做工真的很扎实。裙摆是A字的微微伞摆，你看我转一下...（转了一圈）你看它飘起来那个弧度，而且腰线这里有一个隐藏的松紧设计...（右手捏了捏腰部）不会勒但又收腰。

### dress / female / en
> I seriously didn't expect this dress to look this good on. The fabric is... (pulls up hem) it's this acetate satin, has actual weight, not cheap at all. And the stitching inside... (flips hem) fully finished seams, no raw edges. The skirt is this subtle A-line flare, watch when I spin... (spins) See how it flows? And the waistband has hidden elastic... (pinches waist) cinches without digging in.

### dress / male / zh
> 说实话这条裙子比我预期好很多。你们看面料...（右手拉起裙摆展示）醋酸缎面的，有厚度有质感，不是那种一看就便宜的料子。做工...（右手翻开内侧给镜头看）全是包边走线，没线头，确实扎实。裙摆A字微伞摆，转一下你们看...（转了一圈）这个弧度很好看。腰线有隐藏松紧...（右手捏了捏腰部）收腰但不勒，设计合理。

### dress / male / en
> Honestly this dress is way better than I expected. Fabric... (pulls up hem) acetate satin, has weight and texture, not cheap. Construction... (flips inside) fully finished seams, no loose threads. A-line flare, watch... (spins) nice arc. Hidden elastic waistband... (pinches waist) cinches without squeezing.

### top / female / zh
> 你看这件上衣，版型真的绝了。肩线...（右手沿着肩缝划过去）是落肩但不是烂大街的那种，刚好在肩头往下一厘米，就...嗯...显得肩膀很窄很精致。面料...（右手拉起下摆展示）260克重磅棉，洗十次都不变形。领口罗纹...（右手轻轻拉了拉领口边）弹性很好，不会越穿越松垮。嗯...腰这里有点收的，但又不太紧...（侧身展示腰线）侧面这个弧度，该收的收，该放的放。

### top / female / en
> Look at this top, the cut is insane. Shoulder seam... (traces along it) drop shoulder, one centimeter below the bone, makes shoulders look narrow and clean. Fabric... (lifts hem) 260gsm heavyweight cotton, won't warp after ten washes. Ribbed collar... (flicks neckline) stretchy, won't sag. Slightly tapered waist... (turns sideways) cinched where it matters.

### top / male / zh
> 这件上衣版型确实不错。肩线...（右手沿肩缝划过去）落肩一厘米，不夸张，穿着自然。面料...（右手拉起下摆展示）260克重磅棉，厚实，洗了不变形。领口罗纹...（右手拉了拉领口）弹性好，不会松垮。腰部微收...（侧身展示）侧面轮廓干净，不松不紧。

### top / male / en
> This top's got a solid cut. Shoulder seam... (traces it) one centimeter drop, natural, not overdone. 260gsm heavyweight cotton... (lifts hem) thick, holds shape after washing. Ribbed collar... (tugs it) stays put. Slight taper at the waist... (turns sideways) clean profile.

### pants / female / zh
> 好...我终于找到了一条不用改裤脚的裤子！你看腰头...（右手翻出腰头内侧展示）双层的，里面还有防滑硅胶条，蹲下去再站起来也不滑。裤型...（退后两步正面展示）直筒微锥的，关键是侧缝线...（右手从腰沿着裤缝往下划）往后偏了一点，视觉上让腿看起来更直更长。面料...（右手抓起裤腿揉了揉再松开）松手就回弹，有弹力的西装面料，坐一天不出褶子。九分长度，裤脚收边干净。

### pants / female / en
> Finally... pants I don't need to hem! Waistband... (flips inside) double-layered with silicone grip, stays put. Silhouette... (steps back) straight with slight taper, side seam shifted back... (traces from waist down) makes legs look straighter. Fabric... (scrunches pant leg, releases) bounces right back, stretch suiting, no wrinkles after sitting all day. Ankle length, clean hem.

### pants / male / zh
> 这条裤子几个重点。腰头...（右手翻出内侧展示）双层的，有防滑硅胶条，蹲下站起来不滑。裤型...（退后两步展示）直筒微锥，侧缝线...（右手从腰沿裤缝往下划）往后偏了一点，视觉上腿更直。面料...（右手抓起裤腿揉一下松开）松手回弹，有弹力西装面料，坐一天不起皱。九分长度，收边干净利落。

### pants / male / en
> Key points on these pants. Waistband... (flips inside) double-layered, silicone grip strip. Straight taper... (steps back) side seam shifted back, visually lengthening. Fabric... (scrunches and releases) snaps back, stretch suiting, wrinkle-free. Ankle length, clean hem.

### jacket / female / zh
> 天哪...穿上之后照镜子就...哇，气场直接出来了。面料...（右手蹭了蹭袖子）挺括的华达呢，磨砂感但不扎人，很有分量，拿手上就知道不便宜。肩线...（右手拍了拍肩膀）两毫米微垫肩，不夸张，刚好撑起来不塌。内衬...（拉开外套给镜头看）缎面的，滑进去很爽。扣子...（右手拨弄前襟纽扣）真正牛角扣，不是塑料。

### jacket / female / en
> Oh my god... instant power the moment I put it on. Fabric... (rubs sleeve) structured gabardine, has real weight. Shoulder... (pats shoulder) two millimeters of padding, just enough structure. Lining... (opens jacket) satin, slides right on. Buttons... (fiddles with button) real horn, not plastic.

### jacket / male / zh
> 这件外套穿上就知道不便宜。面料...（右手蹭了蹭袖子）华达呢，挺括有分量，磨砂质感但不扎。肩线...（右手拍肩膀）两毫米微垫肩，撑得起来但不夸张。内衬...（拉开外套展示）缎面，穿脱顺滑。扣子...（右手拨弄纽扣）牛角扣，不是塑料。做工细节到位。

### jacket / male / en
> You can tell this jacket's quality the second you put it on. Gabardine... (rubs sleeve) structured, has weight, matte finish. Shoulder... (pats it) minimal padding, holds shape without overdoing it. Satin lining... (opens jacket) smooth. Horn buttons... (touches button) not plastic. Details are there.

### suit / female / zh
> 这套...嗯...我自己打十分。先说上衣...领子...（右手拉着西装领子）戗驳领，角度锐利，显得人很精神。胸袋...（右手划过胸口口袋）斜插的，比直的显瘦。裤子和上衣同一块面料...（右手把上衣下摆贴着裤腰对比）色差完全一致。转一圈...（转身展示背面）后背没多余褶皱，单开衩，更正式更有质感。

### suit / female / en
> Giving this suit a solid ten. Blazer collar... (tugs lapel) peak lapel, sharp angle, looks polished. Breast pocket... (traces it) angled, more slimming. Same bolt of fabric... (holds hem against waistband) perfect match. Let me spin... (turns) clean back, single vent, refined.

### suit / male / zh
> 这套直接给满分。上衣...（右手拉西装领子）戗驳领，角度锐利，精气神马上就有了。胸袋...（右手划过口袋）斜插，视觉显瘦。裤子上衣同料裁的...（右手对比上下面料）色差为零。转一下...（转身）后背干净利落，单开衩，够正式。

### suit / male / en
> Full marks on this suit. Peak lapel... (tugs collar) sharp angle, instant presence. Angled breast pocket... (traces it) slimming. Same fabric top to bottom... (compares) zero color difference. Back is clean... (turns) single vent, formal.

### casual / female / zh
> 今天就一个超日常的穿搭，出门买咖啡遛弯那种。但这件T...（右手拉起衣角展示）不是普通白T，克重...拿手上沉甸甸的，领口是小圆领，开口不大...（右手轻拉领口）不会洗几次就变大。下面裤子...面料...（右手揉了揉裤腿）棉麻混纺，有自然的肌理感，但不扎腿，贴皮肤很舒服。

### casual / female / en
> Super casual today, grab-coffee-and-go look. But this tee... (lifts hem) heavyweight, you can feel it. Small crew neck... (traces collar) won't stretch out. Pants... (rubs pant leg) cotton-linen blend, textured but comfortable.

### casual / male / zh
> 今天走个日常路线。这件T...（右手拉起衣角展示）不是普通白T，拿手上就知道有分量，重磅的。领口...（右手拉了拉领口）小圆领，洗了不变形。裤子...（右手揉裤腿）棉麻混纺，有肌理但不扎，穿着舒服。

### casual / male / en
> Keeping it simple today. This tee... (lifts hem) heavyweight, you feel the quality. Crew neck... (tugs collar) holds its shape. Pants... (rubs leg) cotton-linen, textured but soft.

### default / female / zh
> 嗯...就是之前刷到好多人推荐的那件，我终于买了。面料...（右手拉起衣角展示）你看这个纹理，有肌理感，不是那种滑面化纤，像高支棉的柔软但有骨架感。做工...（右手翻开内侧展示缝线）走线很密很工整，收边是折叠锁边的。版型...（退后一步正面展示）上身轮廓...该贴的贴该松的松，修饰身形但完全不勒。嗯...你看侧面...（侧身展示）腰线位置特别好。

### default / female / en
> I finally got the thing everyone's been recommending. Fabric... (pulls up hem) has texture, not slippery polyester, soft but structured. Construction... (flips inside) dense stitching, folded lock-stitch. Fit... (steps back) drapes perfectly, fitted where it should be. Side view... (turns) waistline sits just right.

### default / male / zh
> 之前一直被推荐这件，终于上手了。面料...（右手拉起衣角展示）有肌理感，不是化纤滑面，类似高支棉的质感。做工...（右手翻开内侧展示）走线密实，折叠锁边，不会穿两次就散。版型...（退后一步展示）上身轮廓干净，该贴的贴该松的松。侧面...（侧身）腰线位置对，不拖沓。

### default / male / en
> Been hearing about this one, finally got it. Fabric... (lifts hem) textured, not synthetic-slick, feels like premium cotton. Construction... (flips inside) tight stitching, folded seams, built to last. Fit... (steps back) clean silhouette. Side view... (turns) waistline sits right, no dragging.

---

## 3. Selling Closings — by (target_audience, garment_type)

### Female audience

| Garment | zh | en |
|---------|----|----|
| dress | 你们猜多少钱？不到两百！超显腿长，闭眼入。 | Guess the price? Under thirty! Makes legs look forever. No-brainer. |
| top | 随便配条牛仔裤、配裙子都行，显肩窄显脸小，闭眼入。 | Pairs with jeans, skirts, anything. Makes shoulders look narrow. Get it. |
| pants | 165配小白鞋刚刚好，显腿长显瘦，真的推荐。 | Perfect with sneakers, slimming and elongating. Highly recommend. |
| jacket | 穿上气场全开，价格还很合理，冲。 | Instant power vibes, and the price is fair. Go for it. |
| suit | 最关键显瘦！我今天吃了火锅出来完全看不出来。 | Most importantly, it's slimming. I just ate a huge meal, can you tell? No. |
| casual | effortless chic，五分钟出门但不邋遢，推荐。 | Effortless chic, five minutes, out the door, still put-together. |
| default | 价格也不贵，真的闭眼入级别了，必须分享给你们。 | Price is right too. Absolute no-brainer. You need this. |

### Male audience

| Garment | zh | en |
|---------|----|----|
| dress | 这个质感在这个价位真的没话说，值得入手。 | Quality at this price point is legit. Worth it. |
| top | 不挑身材不挑场合，耐洗耐穿，闭眼入兄弟们。 | Works on any build, any occasion. Durable. Just get it. |
| pants | 坐一天不起皱，一条能穿好几年，质价比到位。 | Wrinkle-free all day, lasts for years. Worth every penny. |
| jacket | 有型有质感，这个价位确实没毛病。 | Stylish, quality build, fair price. No complaints. |
| suit | 做工扎实，撑得住任何场面，值得入。 | Solid build, holds up in any setting. Worth the investment. |
| casual | 省心不费脑子，穿上出门就完事。 | Zero effort, throw it on, done. That simple. |
| default | 实穿百搭，质价比到位，闭眼入。 | Practical, versatile, solid value. Get it. |

---

## 4. Garment Actions

All actions use RIGHT HAND only. WHY: Seedance has mirror-flip issues; fixing to right hand avoids left/right inconsistency.

| Type | Actions |
|------|---------|
| dress | 右手拉起裙摆展示面料（始终用右手），右手翻开裙摆内侧展示车线做工，小幅转身让裙摆飘动，右手捏腰部展示松紧设计 |
| top | 右手沿肩缝划过展示肩线位置，右手拉起下摆展示面料厚度，右手轻拉领口展示弹性（始终用右手操作），侧身展示腰线弧度 |
| pants | 右手翻出腰头内侧展示防滑条（始终用右手操作），退后两步展示全身裤型，右手沿侧缝线从腰往下划展示裁剪，右手抓起裤腿揉一下再松开展示回弹性 |
| jacket | 右手蹭袖子展示面料质感（始终用右手操作），右手拍肩膀展示垫肩，拉开外套展示缎面内衬，右手拨弄前襟纽扣展示牛角扣 |
| suit | 右手拉西装领子展示戗驳领（始终用右手操作），右手划过胸口口袋展示斜插设计，右手把上衣下摆贴着裤腰对比色差，转身展示背面裁剪和开衩细节 |
| casual | 右手拉起衣角展示面料厚度（始终用右手操作），右手轻拉领口展示开口大小，右手揉裤腿展示棉麻面料质感 |
| default | 右手拉起衣角展示面料（始终用右手操作），右手翻开衣服内侧给镜头看缝线做工，退后一步正面展示整体版型，侧身展示腰线位置 |

## 5. Action Demeanor

| Gender | Demeanor |
|--------|----------|
| female | 面朝镜头表情生动自然地展示服装 |
| male | 面朝镜头自信从容地展示服装 |

## 6. Dialogue Style Instructions (gender-aware)

| Style | Female | Male |
|-------|--------|------|
| natural | 语气自然亲切，像在跟闺蜜视频通话。说话有停顿、有喘息、偶尔磕巴自我纠正，真实感强。 | 语气自然随和，像在跟朋友聊天推荐好物。说话直接但不生硬，偶尔停顿思考，真实感强。 |
| professional | 语气专业自信，像品牌代言人。吐字清晰，节奏稳定。 | 语气专业沉稳，像品牌代言人。吐字清晰，从容有力。 |
| enthusiastic | 语气兴奋热情，像发现了宝藏。语速偏快，情绪感染力强。 | 语气热情有感染力，像发现好东西迫不及待分享。语速适中但有力。 |
