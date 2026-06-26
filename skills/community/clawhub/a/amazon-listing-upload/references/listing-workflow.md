# Amazon Listing Workflow

Step-by-step guide for creating product listings on Amazon Seller Central.

## Pre-Listing Checklist

Before starting, ensure you have:
- [ ] Seller Central account (Professional plan)
- [ ] Product images ready (7 images minimum)
- [ ] GTIN exemption approved OR valid UPC codes
- [ ] Product information compiled (see templates/product-template.txt)
- [ ] Category determined and approved (if gated)
- [ ] Pricing strategy decided
- [ ] Fulfillment method chosen (FBA vs FBM)

## Step 1: Navigate to Add Products

1. Log into Seller Central
2. Go to **Inventory** → **Add Products**
3. Choose one of:
   - "I'm adding a product not sold on Amazon" (new product)
   - "I want to select an existing product" (existing ASIN)

## Step 2: Select Product Category

### Finding the Right Category

**Method A: Browse Categories**
1. Click through category tree
2. Select most specific subcategory possible
3. Note if approval is required

**Method B: Search by Product Name**
1. Enter product name/type
2. Amazon suggests categories
3. Select best match

**Important**: Category determines:
- Referral fees
- Listing requirements
- Search visibility
- Competition level

## Step 3: Fill Vital Information

### Product Name (Title)
```
Template: [Brand] + [Product] + [Key Feature] + [Size/Count]

Example:
Wondermed Liver Support Complex - 5-in-1 Milk Thistle Supplement 
with Artichoke & Dandelion - 120 Capsules - Made in USA
```

**Requirements:**
- Max 200 characters (varies by category)
- Capitalize first letter of each word (except prepositions)
- Include brand name at beginning
- No promotional phrases (Best, Top, #1)
- No special characters (! * $ ?)

### Brand Name
- Must match GTIN exemption exactly (if applicable)
- Consistent across all listings
- Will display on product page

### Product ID

**If you have UPC:**
1. Select "UPC" from dropdown
2. Enter 12-digit code
3. Verify with barcode scanner if possible

**If using GTIN Exemption:**
1. Select "GTIN" from dropdown
2. Check box: "Does not have a Product ID"
3. System will use exemption from your account

### Other Vital Fields
- **Manufacturer**: Your company name or brand
- **Model Number**: Internal SKU (WND-LVR-120-01)
- **Model Name**: Product line name
- **Item Type Keyword**: Category-specific keyword

## Step 4: Variations (If Applicable)

### When to Use Variations
- Same product, different sizes
- Same product, different colors
- Same product, different quantities

### Variation Structure
```
Parent Listing: Generic product information
├── Child 1: Size Small, Red
├── Child 2: Size Small, Blue
├── Child 3: Size Large, Red
└── Child 4: Size Large, Blue
```

### Setup Process
1. Select "This product has variations"
2. Choose variation theme (Size, Color, SizeColor)
3. Enter variation values
4. Fill information for each child

**Note**: Each child needs its own SKU and inventory count

## Step 5: Offer Information

### Pricing
- **Your Price**: Regular selling price
- **Sale Price**: Promotional price (optional)
- **Sale Dates**: When promotion runs (optional)

### Inventory
- **Quantity**: Units available
- **Fulfillment Channel**:
  - Amazon (FBA)
  - Merchant (FBM)
- **Handling Time**: Days to ship (FBM only)
- **Condition**: New, Used, Refurbished

### Seller SKU
Internal tracking code. Format suggestions:
```
BRAND-CATEGORY-001-VARIANT
WND-LVR-120-01
WND-LVR-120-02 (for variations)
```

## Step 6: Product Description

### Key Product Features (Bullet Points)

**Format:**
```
[ALL CAPS HEADER] Detailed benefit description with keywords.
```

**Example:**
```
[ULTIMATE 5-IN-1 LIVER MATRIX] Experience comprehensive liver support 
with our synergistic blend of Milk Thistle (250mg), Artichoke, Dandelion 
Root, Yarrow, and Burdock Root. This potent formula is designed to assist 
your body's natural cleansing processes.
```

**Requirements:**
- Exactly 5 bullet points
- Max 500 characters each
- Start with key benefit
- Include relevant keywords naturally
- Focus on customer benefits, not just features

### Product Description (HTML)

**Structure:**
```html
<p><strong>[Hook/Headline]</strong></p>
<p>[Introduction paragraph]</p>
<p><strong>Why Choose [Brand]?</strong></p>
<ul>
  <li><strong>Feature 1:</strong> Benefit explanation</li>
  <li><strong>Feature 2:</strong> Benefit explanation</li>
</ul>
<p><strong>[Value Proposition]</strong></p>
<p>[Additional details]</p>
```

**Allowed HTML Tags:**
- `<p>` - Paragraph
- `<br>` - Line break
- `<ul>`, `<li>` - Bulleted lists
- `<strong>`, `<b>` - Bold
- `<em>`, `<i>` - Italic

**Max Length:** 2000 characters

### Backend Search Terms

**Format:**
```
keyword1,keyword2,keyword3,keyword4
```

**Rules:**
- Max 250 bytes (not characters)
- No repetition
- No brand names
- No ASINs
- No subjective claims

**Example:**
```
silymarin,milk thistle capsules,liver detoxifier,herbal supplement,
artichoke extract,dandelion root,metabolism support,digestive health
```

## Step 7: Upload Images

### Upload Order
1. Main Image (required, white background)
2. Infographic 1
3. Infographic 2
4. Lifestyle
5. Detail/Feature
6. Scale/Dimensions
7. Packaging

### Technical Requirements
- Format: JPEG, TIFF, PNG, GIF
- Size: Minimum 1000 x 1000 px
- Color: sRGB
- File size: Max 10MB per image

### Main Image Requirements
- Pure white background (RGB 255,255,255)
- Product fills 85%+ of frame
- No text, logos, watermarks
- No props or accessories
- Professional quality

## Step 8: More Details

### Compliance Information
- **Country of Origin**: Where manufactured
- **Legal Disclaimer**: Required for supplements
- **Directions**: Usage instructions
- **Ingredients**: Full list for supplements/food

### Specifications
- **Unit Count**: Number of units (120)
- **Unit Count Type**: Type (Capsules, Ounces, etc.)
- **Material Feature**: Non-GMO, Organic, etc.
- **Item Form**: Capsule, Liquid, Powder, etc.

### Dimensions (if applicable)
- Package dimensions
- Item dimensions
- Weight

## Step 9: Review and Submit

### Pre-Submission Checklist
- [ ] Title within character limit
- [ ] Main image pure white background
- [ ] All required fields completed
- [ ] No spelling errors
- [ ] Pricing correct
- [ ] Inventory quantity accurate
- [ ] Category correct

### Submit Listing
1. Click "Save and Finish"
2. Wait for submission confirmation
3. Note the ASIN assigned (if new listing)

## Step 10: Post-Submission

### Timeline
- **New listing review**: 15 minutes - 24 hours
- **Suppressed listing check**: Immediate
- **Buy Box eligibility**: 24-48 hours

### Monitor Status
1. Go to **Inventory** → **Manage Inventory**
2. Check listing status:
   - **Active**: Listing is live
   - **Inactive**: Check for issues
   - **Suppressed**: Fix required fields

### Common Issues

**Suppressed Listing:**
- Missing required fields
- Main image doesn't meet requirements
- Title too long
- Missing category approval

**Search Suppressed:**
- Missing search terms
- Category/browse node issues
- Brand name issues

## FBA Setup (If Using FBA)

### Create Shipping Plan
1. **Inventory** → **Manage FBA Inventory**
2. Click **Send/Replenish Inventory**
3. Select your SKU
4. Enter quantity to send
5. Create new shipping plan

### Prepare Shipment
1. **Who preps?** Choose Amazon (fee applies) or Merchant
2. **Labeling**: Print FNSKU labels
3. **Packaging**: Follow FBA prep requirements
4. **Shipping**: Choose Amazon Partnered Carrier or your own

### Track Shipment
- Monitor in **Inventory** → **Manage FBA Shipments**
- Watch for:
  - Check-in status
  - Receiving status
  - Available inventory

## Listing Optimization

### After Listing is Live

**Week 1:**
- Monitor for customer questions
- Check search results ranking
- Verify images display correctly
- Confirm pricing competitiveness

**Month 1:**
- Gather initial reviews
- Analyze conversion rate
- Optimize keywords based on search terms report
- Adjust pricing if needed

### A/B Testing
Amazon doesn't support true A/B testing, but you can:
- Change one element at a time
- Monitor for 2 weeks minimum
- Track sessions and conversion rate
- Use Brand Analytics (if registered)

## Resources

### Amazon Help Pages
- Add a Product Help
- Image Requirements
- Category Style Guides
- FBA Prep Requirements

### Tools
- **Listing Quality Dashboard**: Check for improvements
- **Brand Analytics**: Search terms and market basket
- **Manage Your Experiments**: A/B testing (brands only)

---

*Workflow updated March 2026. Interface may vary slightly.*
