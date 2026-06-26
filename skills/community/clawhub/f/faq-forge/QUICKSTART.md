# FAQ Forge - Quick Start Guide

**Get your FAQ up and running in 5 minutes!**

---

## Prerequisites

- Python 3.6+ installed
- That's it! No dependencies needed.

---

## Installation

```bash
# Download/clone FAQ Forge
cd faq-forge

# Verify installation
python3 test_demo.py
```

You should see "ALL TESTS PASSED!" 🎉

---

## Option 1: Start with a Template (Recommended)

### Step 1: Choose Your Template

```bash
python3 faq_templates.py list
```

Available templates:
- `digital-products` - Ebooks, courses, software
- `saas` - Web apps, subscription services
- `freelance` - Services, consulting
- `ecommerce` - Physical products, online stores

### Step 2: Apply Template

```bash
# Example: digital products business
python3 faq_templates.py apply digital-products
```

### Step 3: Customize Answers

```bash
# See what was created
python3 faq_forge.py list

# Update an answer
python3 faq_forge.py update how-do-i-access-my-purchase-after-buying \
  --answer "Your customized answer here"
```

### Step 4: Publish

```bash
python3 faq_publish.py html faq.html
```

Open `faq.html` in your browser! ✨

---

## Option 2: Start from Scratch

### Step 1: Add Your First Question

```bash
python3 faq_forge.py add \
  "How do I contact support?" \
  "Email us at support@yourbusiness.com or use the contact form on our website." \
  --category "Support" \
  --tags "contact,help" \
  --priority "high"
```

### Step 2: Add More Questions

```bash
python3 faq_forge.py add \
  "What payment methods do you accept?" \
  "We accept Visa, Mastercard, PayPal, and Apple Pay." \
  --category "Billing" \
  --tags "payment,billing"

python3 faq_forge.py add \
  "What is your refund policy?" \
  "We offer a 30-day money-back guarantee. Contact support for refunds." \
  --category "Billing" \
  --tags "refund,policy" \
  --priority "high"
```

### Step 3: Publish

```bash
python3 faq_publish.py html faq.html
```

---

## Option 3: Import from Existing Docs

### If You Have Markdown Files

```bash
python3 faq_import.py markdown your_existing_faq.md \
  --category "General"
```

### If You Have a Folder of Docs

```bash
python3 faq_import.py directory ./docs \
  --category "Documentation"
```

Then review and publish:

```bash
python3 faq_forge.py list
python3 faq_publish.py html faq.html
```

---

## Essential Commands

### Add a Question
```bash
python3 faq_forge.py add "Question?" "Answer" \
  --category "Category Name" \
  --tags "tag1,tag2" \
  --priority "high"
```

### Search Questions
```bash
python3 faq_forge.py search "keyword"
python3 faq_forge.py search --category "Billing"
```

### Update an Answer
```bash
python3 faq_forge.py update question-id \
  --answer "New improved answer"
```

### Publish HTML
```bash
python3 faq_publish.py html output.html
```

### See All Questions
```bash
python3 faq_forge.py list
```

### Get Statistics
```bash
python3 faq_forge.py stats
```

---

## Publishing Options

### HTML (Recommended)
```bash
python3 faq_publish.py html faq.html \
  --title "Customer Support FAQ"
```
✅ Searchable, collapsible, professional design  
✅ Works on any web server (no backend needed)  
✅ Mobile-responsive

### Markdown
```bash
python3 faq_publish.py markdown faq.md
```
✅ Perfect for GitHub wikis  
✅ Documentation sites (GitBook, MkDocs)

### Plain Text
```bash
python3 faq_publish.py text faq.txt
```
✅ Email templates  
✅ Print documentation

---

## Tips for Great FAQs

1. **Start with templates** - Customize from a solid base
2. **Use priorities** - Mark common questions as "high"
3. **Add tags** - Makes searching easier
4. **Link related questions** - Help users find answers
5. **Keep updating** - FAQs should evolve with your business

---

## Example Workflow

```bash
# Day 1: Setup
python3 faq_templates.py apply saas
python3 faq_forge.py list

# Day 2: Customize
python3 faq_forge.py update entry-id --answer "Custom answer"
python3 faq_forge.py add "New question?" "New answer"

# Day 3: Publish
python3 faq_publish.py html public/faq.html
# Upload faq.html to your website

# Ongoing: Maintain
python3 faq_forge.py search --category "Billing"
python3 faq_forge.py update entry-id --answer "Updated answer"
python3 faq_publish.py html public/faq.html
```

---

## Configuration (Optional)

Want to customize categories, colors, or business info?

```bash
cp config_example.json config.json
# Edit config.json with your preferences
```

See `config_example.json` for all options.

---

## Getting Help

- **Full docs:** `README.md`
- **Known issues:** `LIMITATIONS.md`
- **Test installation:** `python3 test_demo.py`

---

## Common Questions

**Q: Do I need to install anything?**  
A: Just Python 3.6+. No pip packages needed!

**Q: Where is my data stored?**  
A: In `faq_data.json` in the current directory.

**Q: Can I use this commercially?**  
A: Yes! MIT License. Use it however you want.

**Q: Can I customize the HTML design?**  
A: Yes! Edit `faq_publish.py` or change colors in `config.json`.

**Q: How do I backup my FAQs?**  
A: Store `faq_data.json` in Git, or export: `python3 faq_import.py export backup.json`

---

## What's Next?

After you're comfortable with the basics:

- Link related questions: `python3 faq_forge.py relate id1 id2`
- Track feedback: `python3 faq_forge.py feedback id --needs-improvement`
- Multi-product FAQs: Use `--product` flag
- Automation: Script it! All commands are scriptable

---

**Ready to build your FAQ?**

```bash
# Choose one:
python3 faq_templates.py apply digital-products
# OR
python3 faq_forge.py add "Your first question?" "Your first answer"

# Then publish:
python3 faq_publish.py html faq.html
```

🚀 **You're all set!**

For complete documentation, see `README.md`.
