# Camera Recommendation Skill

## Description
An AI skill that provides personalized camera purchase recommendations based on user needs, budget, and usage scenarios.

## Trigger Phrases
- "推荐相机"
- "买相机"
- "相机购买"
- "选相机"
- "camera recommendation"
- "recommend a camera"

## Skill Instructions

When this skill is triggered, follow this process:

1. **Analyze User Needs**
   - Identify budget range
   - Determine primary use cases (portraits, landscapes, video, travel, etc.)
   - Assess skill level (beginner, intermediate, professional)
   - Note portability requirements
   - Identify brand/system preferences

2. **Select Appropriate Price Range**
   - 3000-5000元: Compact cameras or entry-level mirrorless kits
   - 5000-8000元: Mid-range APS-C mirrorless or entry full-frame kits
   - 8000-15000元: Mid-range full-frame bodies or pro APS-C
   - 15000-30000元: High-end full-frame with pro lenses
   - 30000元以上: Professional flagship with premium lenses

3. **Match to Use Scenario**
   - Portraits: Full-frame + large aperture prime lenses
   - Landscapes: High megapixel full-frame + wide-angle zoom
   - Video: Strong autofocus + 4K 60fps capability
   - Travel/Everyday: Compact + versatile zoom range

4. **Create Recommendation**
   Provide 2-3 different options with:
   - Camera body (brand, model, price)
   - Lens(es) (focal length, aperture, price)
   - Accessories (optional items, price)
   - Total price
   - Recommendation rationale (2-3 sentences highlighting advantages)

5. **Provide Buying Advice**
   - Recommended purchase channels (official stores, authorized dealers)
   - Important considerations (warranty, inspection, return policies)
   - Additional resources (reviews, tutorials, comparisons)

## Knowledge Base

### Key Concepts
- **Sensor Sizes**: Full-frame > APS-C > M4/3 > 1-inch
- **Lens Mounts**: RF (Canon), Z (Nikon), E (Sony), X (Fujifilm), M (M4/3)
- **Key Parameters**: Megapixels, burst rate, autofocus points, video specs, IBIS, weather sealing

### Common Camera Models by Price

**3000-5000元**
- Sony RX100 series, Canon G7X
- Canon EOS R50 kit, Nikon Z30 kit

**5000-8000元**
- Fujifilm X-T50, Sony A6400
- Canon EOS RP kit, Nikon Z5 kit

**8000-15000元**
- Canon EOS R8, Sony A7III
- Fujifilm X-H2S, Sony A6700

**15000-30000元**
- Sony A7IV, Canon EOS R6 Mark II
- Pro zoom lenses (24-70mm f/2.8, 70-200mm f/2.8)

**30000元以上**
- Sony A7RV, Canon EOS R5, Nikon Z8
- Professional lens collections

### Use Case Recommendations

**Portraits**
- Recommended: Full-frame + 85mm f/1.8 or 50mm f/1.8
- Example: Canon EOS R8 + RF 85mm f/2

**Landscapes**
- Recommended: High-res full-frame + 16-35mm wide-angle
- Example: Sony A7RV + Sony 16-35mm f/2.8 GM

**Video**
- Recommended: Strong AF + 4K 60fps, external recording support
- Example: Sony A7SIII, Canon EOS R5

**Travel/Everyday**
- Recommended: Compact + versatile zoom (18-150mm or 18-300mm)
- Example: Canon EOS R50 + RF-S 18-150mm, Sony RX100 VII

## Output Format

```
📷 **Camera Recommendation for [User]**

**📊 Needs Analysis**
- Budget: [Amount]
- Main Uses: [Scenario 1, Scenario 2, ...]
- Skill Level: [Beginner/Intermediate/Professional]
- Portability: [Required/Normal/Not Important]

**🎯 Recommended Options**

**Option 1: [Name] - [Total Price]**
- Body: [Brand Model] - [Price]
- Lens: [Brand Model] - [Price]
- Accessories: [List] - [Price]
- Total: [Sum]
- Why Recommended: [2-3 sentences explaining advantages]

**Option 2: [Name] - [Total Price]**
- [Same structure]

**📝 Buying Advice**
- Where to Buy: [Platform/Store]
- Important Notes: [Inspection, warranty, etc.]
- Further Reading: [Review/tutorial links]
```

## Examples

### Example 1: Beginner Portrait Photography
**User**: "我是摄影新手,想拍人像,预算8000元左右"

**Response**:
```
📷 **Beginner Portrait Photography Solution**

**📊 Needs Analysis**
- Budget: ¥8,000
- Main Uses: Portrait photography
- Skill Level: Beginner
- Portability: Normal

**🎯 Recommended Options**

**Option 1: Canon EOS R8 + RF 50mm f/1.8 - ~¥8,500**
- Body: Canon EOS R8 - ~¥6,800
- Lens: RF 50mm f/1.8 STM - ~¥1,000
- Accessories: SD card, camera bag - ~¥700
- Total: ¥8,500
- Why Recommended: Excellent image quality, fast autofocus, great portrait colors, easy to use for beginners

**Option 2: Sony A6400 + 50mm f/1.8 - ~¥7,500**
- Body: Sony A6400 - ~¥5,200
- Lens: Sony 50mm f/1.8 OSS - ~¥1,500
- Accessories: SD card, camera bag - ~¥800
- Total: ¥7,500
- Why Recommended: Top-tier autofocus performance, extensive lens ecosystem, great value for money

**📝 Buying Advice**
- Where to Buy: JD.com Self-owned, Tmall Official Flagship Store
- Important Notes: Check warranty policy, inspect sensor cleanliness upon delivery
```

### Example 2: Professional Video Production
**User**: "我是专业视频创作者,需要拍摄4K视频,预算5万"

**Response**:
```
📷 **Professional Video Production Solution**

**📊 Needs Analysis**
- Budget: ¥50,000
- Main Uses: Professional video production
- Skill Level: Professional
- Portability: Normal

**🎯 Recommended Options**

**Option 1: Sony A7SIII + 24-70mm f/2.8 GM - ~¥48,000**
- Body: Sony A7SIII - ~¥24,000
- Lens: Sony FE 24-70mm f/2.8 GM II - ~¥18,000
- Accessories: External recorder, microphone, gimbal - ~¥6,000
- Total: ¥48,000
- Why Recommended: Professional video specs, 10-bit 4:2:2, excellent low-light performance

**Option 2: Canon EOS R5 + RF 24-70mm f/2.8L - ~¥46,000**
- Body: Canon EOS R5 - ~¥24,000
- Lens: Canon RF 24-70mm f/2.8L IS USM - ~¥16,000
- Accessories: External recorder, microphone, gimbal - ~¥6,000
- Total: ¥46,000
- Why Recommended: 8K video, superior image stabilization, excellent color science

**📝 Buying Advice**
- Where to Buy: Authorized dealers, JD.com Self-owned
- Important Notes: Video recording time limits, consider cooling solutions
```

## Limitations

- Prices may fluctuate; verify before purchasing
- Cannot provide real-time inventory information
- Individual experiences may vary
- New models may have initial availability issues

## Updates

This skill will be regularly updated with:
- New camera releases
- Price changes
- User reviews and feedback
- Market trends

**Last Updated**: March 2026
**Region**: China Mainland
**Currency**: Chinese Yuan (CNY)
