<p align="center">
  <strong>🌐 اللغات:</strong>
  <a href="README.zh.md">中文</a> |
  <a href="README.en.md">English</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.ar.md">العربية</a>
</p>

# Agent PaddleOCR Vision —— فهم الوثائق وإجراءات العامل باستخدام PaddleOCR

**حوّل المستندات إلى تعليمات قابلة للتنفيذ لوكلاء الذكاء الاصطناعي.** تعتمد هذه الأداة exclusively على واجهة برمجة التطبيقات السحابية لـ PaddleOCR، وتصنف أنواع المستندات تلقائيًا وتوفر اقتراحات بارامترات منظمة وموجهة.

## نظرة عامة على الميزات

- التعرف البصري على الأحرف (OCR) عبر PaddleOCR السحابي (يدعم الجداول والمعادجات واللغات المتعددة)
- التصنيف التلقائي لـ 15 نوع مستند: invoice, business_card, receipt, table, contract, id_card, passport, bank_statement, driver_license, tax_form, financial_report, meeting_minutes, resume, travel_itinerary, general
- إعادة محاولة تلقائية عند أخطاء 5xx/مهلة
- معالجة دفعات بالتوازي (خيار `--workers`)
- تصدير CSV (`--format csv`)
- عرض مُنسَّق للبشر (`--format pretty`)
- تولد اقتراحات إجراءات لكل نوع (create_expense, add_contact, summarize، إلخ)
- معالجة دفعات (Batch) لدلائل كاملة
- توليد PDFs ذات طبقة نصية قابلة للبحث (بناءً على إحداثيات المربعات المحيطة، تدعم تحديد النص والبحث)
- تُنتج `extracted_fields` بيانات منظمة لاستخدامها مباشرة من قبل العامل

## التثبيت

### متطلبات النظام

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip poppler-utils
```

macOS:

```bash
brew install python poppler
```

### حزم Python

```bash
cd skills/agent-paddleocr-vision
pip3 install -r scripts/requirements.txt
```

### إعداد API PaddleOCR

يجب تعيين متغيرين بيئيين:

```bash
export PADDLEOCR_DOC_PARSING_API_URL=https://your-api.paddleocr.com/layout-parsing
export PADDLEOCR_ACCESS_TOKEN=your_access_token
```

*ملاحظة: يجب أن تنتهي رابط API بـ `/layout-parsing`.*

## الاستخدام

### مستند فردي

```bash
# استخدام أساسي: معالجة صورة أو PDF، وإخراج JSON pretty
python3 scripts/doc_vision.py --file-path ./invoice.jpg --pretty

# إنشاء PDF قابل للبحث أيضًا
python3 scripts/doc_vision.py --file-path ./document.pdf --make-searchable-pdf --output result.json

# نص فقط
python3 scripts/doc_vision.py --file-path ./doc.pdf --format text
```

### المعالجة بالدفعات (Batch)

```bash
# معالجة جميع الملفات المدعومة في دليل (.pdf, .png, .jpg, .jpeg, .bmp, .tiff, .webp)
python3 scripts/doc_vision.py --batch-dir ./inbox --output-dir ./out
```

نتائج الدفعات:
- يتم إنشاء JSON ملخص (يشمل العدد الإجمالي، عدد النجاح/الفشل، إحصائيات حسب النوع)
- كل ملف يحصل على JSON خاص به في `--output-dir`

### Docker

```bash
docker build -t agent-paddleocr-vision:latest .
docker run --rm -v $(pwd)/data:/data \
  -e PADDLEOCR_DOC_PARSING_API_URL -e PADDLEOCR_ACCESS_TOKEN \
  agent-paddleocr-vision:latest \
  --file-path /data/invoice.jpg --pretty --make-searchable-pdf
```

## تنسيق الإخراج

```json
{
  "ok": true,
  "document_type": "invoice",
  "confidence": 0.94,
  "text": "النص المستخرج كامل (الصفحات مفصولة بسطرين جديدين)",
  "pruned_result": { ... هيكل رد الخام من PaddleOCR ... },
  "suggested_actions": [
    {
      "action": "create_expense",
      "description": "سجل هذه الفاتورة في النظام المحاسبي",
      "parameters": {
        "amount": "1200",
        "vendor": "某某科技有限公司",
        "date": "2025-03-15",
        "tax_id": "12345678"
      },
      "confidence": 0.92
    },
    {
      "action": "archive",
      "description": "أرشفة هذه الفاتورة في مكتبة المستندات",
      "parameters": {},
      "confidence": 0.96
    },
    {
      "action": "tax_report",
      "description": "ضيفها لتقرير الضرائب الحالي",
      "parameters": { "tax_period": "2025-03" },
      "confidence": 0.78
    }
  ],
  "extracted_fields": {
    "amount": "1200",
    "vendor": "某某科技有限公司",
    "date": "2025-03-15"
  },
  "top_action": "create_expense",
  "metadata": {
    "pages": 1,
    "backend": "paddleocr",
    "source": "/مسار/مطلق/للفاتورة.jpg"
  },
  "searchable_pdf": "/مسار/مطلق/للفاتورة.searchable.pdf"
}
```

### مرجع الحقول

| الحقل | الوصف |
|------|-------|
| ok | ما إذا كان المعالجة ناجحة |
| document_type | نوع المستند (invoice, business_card, ...) |
| confidence | درجة ثقة التصنيف (0–1) |
| text | كل النص المستخرج من كل الصفحات (تنسيق Markdown) |
| pruned_result | رد API الخام؛ يحتوي على layoutParsingResults لكل صفحة للمعالجة المتقدمة |
| suggested_actions | قائمة بالإجراءات المقترحة، مرتبة حسب الثقة |
| extracted_fields | بيانات منظمة (المبلغ، التاريخ، البائع، إلخ) للاستخدام المباشر |
| top_action | اسم الإجراء الأعلى ثقة |
| metadata | يتضمن عدد الصفحات، نوع النهاية الخلفية، مصدر المسار، إلخ |
| searchable_pdf | مسار PDF ذو طبقة نصية (يظهر فقط عند استخدام `--make-searchable-pdf`) |

## دمج الوكيل (Agent)

1. **استخدم `extracted_fields`**: الوصول مباشرة إلى البيانات المنظمة (المبلغ، التاريخ، البائع، إلخ).
2. **توفير أزرار تفاعلية**: حوّل `suggested_actions` إلى أزرار رد سريعة.
3. **تنفيذ تلقائي**: بعد التأكيد، استدعِ الدالة مع `parameters` من `suggested_actions`.

مثال (شفرة تشبه Node.js):

```javascript
const result = await callAgentVision({ 'file-path': '/مسار/المستند.pdf' });
if (result.document_type === 'invoice') {
  for (const act of result.suggested_actions) {
    showButton(act.description, { action: act.action, params: act.parameters });
  }
}
```

## PDF ذو طبقة نصية قابلة للبحث

`--make-searchable-pdf` ينشئ PDF جديد به طبقة نصية يمكن اختيارها والبحث فيها. كيف يعمل:

1. تُحوَّل كل صفحة من PDF المدخل إلى صورة نقطية بدقة 200 DPI (باستخدام `pdf2image` و `poppler` بالنظام)
2. بناءً على إحداثيات `bbox` للقطع الصغيرة من `layoutParsingResults[].prunedResult` لـ PaddleOCR، يُوضع نص غير مرئي في المواقع المقابلة (باستخدام `reportlab`)
3. تبقى الصورة كخلفية؛ تُوضع طبقة النص فوقها. ستطابق قراءات PDF النص المضمن.

إذا لم تُرجع API أي bounding boxes، سينتج الإصدار الاحتياطي نص الصفحة ككل في الأسفل؛ يكون قابلاً للبحث ولكن مواقع النص غير دقيقة.

### البرمجيات المطلوبة

- النظام: `poppler-utils` (Ubuntu: `apt-get install poppler-utils`; macOS: `brew install poppler`)
- Python: `reportlab`, `pypdf`, `pillow`, `pdf2image`

## أنواع المستندات والإجراءات

| النوع | التحديد | الإجراءات المقترحة |
|------|----------|-------------------|
| الفاتورة (invoice) | رقم الفاتورة، المبلغ، رقم الضريبي، البائع/المشتري | create_expense, archive, tax_report |
| بطاقة العمل (business_card) | الاسم، الهاتف، البريد الإلكتروني، الوظيفة | add_contact, save_vcard |
| الإيصال (receipt) | اسم المحل، المبلغ المدفوع، تاريخ المعاملة | create_expense, split_bill |
| الجدول (table) | خطوط الشبكة، متعدد الأعمدة، رؤوس الأعمدة | export_csv, analyze_data |
| العقد (contract) | أرقام البنود، التوقيعات، تاريخ السريان | summarize, extract_dates, flag_obligations |
| بطاقة الهوية (id_card) | رقم الهوية، الاسم، تاريخ الميلاد، الجنس | extract_id_info, verify_age |
| جواز السفر (passport) | رقم الجواز، الجنسية، تواريخ الإصدار/الانقضاء | store_passport_info, check_validity |
| كشف الحساب (bank_statement) | رقم الحساب، فترة الكشف، الرصيد، سجل المعاملات | categorize_transactions, generate_report |
| رخصة القيادة (driver_license) | رقم الرخصة، الصف، الانقضاء، العنوان | store_license_info, check_expiry |
| النموذج الضريبي (tax_form) |年度 الضريبي، إجمالي الدخل، الضريبة المستحقة، الخصومات | summarize_tax, suggest_deductions |
| عام (general) | لا نمط محدد | summarize, translate, search_keywords |
| تقرير مالي (financial_report) | الإيرادات، الأرباح، الهوامش | summarize_financials, compare_periods, flag_risks |
| محضر اجتماع (meeting_minutes) | الحضور، القرارات، المهام | extract_action_items, create_calendar_events, send_summary |
| السيرة الذاتية (resume) | الاسم، البريد، التعليم، المهارات | create_candidate_profile, match_jobs, extract_skills |
| خطة سفر (travel_itinerary) | رحلات جوية، فنادق، تواريخ | create_calendar_events, set_reminders, check_visa |

## استكشاف الأخطاء وإصلاحها

### API PaddleOCR تُرجع 403 أو 404

تحقق من:
- `PADDLEOCR_DOC_PARSING_API_URL` صحيحة وتنتهي بـ `/layout-parsing`
- `PADDLEOCR_ACCESS_TOKEN` صالحة وغير منتهية
- اتصال الشبكة إلى نقطة نهاية API

### فشل إنشاء PDF قابل للبحث

تأكد من تثبيت:
```bash
pip3 show reportlab pypdf pdf2image
```
وتأكد من وجود `poppler` في النظام:
```bash
which pdftoppm  # يجب أن يوجد
```

إذا استمر الفشل، راجع `stderr` للأخطاء؛ أسباب شائعة:
- PDF الإدخال تالف أو مشفر
- بيانات bounding box مفقودة (لا يزال ي生成 لكن موضع النص تقريبي)

### جودة OCR منخفضة

- تأكد من وضوح المستند، إضاءة جيدة، تباين عالٍ
- بالنسبة للصينية، PaddleOCR يدعمها؛ لغات أخرى عادة تُكتشف تلقائيًا
- زد DPI للمصدر (موصى به 300+)

### المعالجة بالدفعات بطيئة

- فكر في المعالجة المتوازية (مثل GNU parallel)
- إذا كنت تستخدم API سحابية، احترم حدود المعدل؛ زد timeout أو قسم إلى دفعات أصغر

## العمارة المعمارية

```
doc_vision.py  →  نقطة الدخول الرئيسية
   ├─ ocr_engine.py      → يستدعي API PaddleOCR، يرجع نص + pruned_result
   ├─ classify.py        → تصنيف نوع المستند بناءً على محتوى النص
   ├─ actions.py         → يستخرج البارامترات ويولد قائمة الإجراءات المقترحة
   ├─ (بدون قوالب)       → بيانات منظمة مباشرة، لا حاجة للقوالب
   └─ make_searchable_pdf.py → ينشئ PDF ذو طبقة نصية باستخدام إحداثيات bbox
```

## تطوير أنواع مستندات جديدة

1. في `scripts/classify.py`، أضِد دالة مطابقة وثابت:
   ```python
   DOC_TYPE_MY_TYPE = "my_type"
   def match_my_type(text: str) -> float:
       patterns = [r"كلمة_مفتاحية1", r"كلمة_مفتاحية2"]
       return sum(bool(re.search(p, text, re.IGNORECASE)) for p in patterns) / len(patterns)
   ```
   ثم أضف `DOC_TYPE_MY_TYPE: match_my_type(text)` إلى قاموس `scores` في `classify()`.

2. في `scripts/actions.py`، أضف دالة مولد:
   ```python
   def suggest_my_type(text: str, metadata) -> List[Action]:
       # استخراج البارامترات، إرجاع قائمة Action
       ...
   SUGGESTION_DISPATCH[DOC_TYPE_MY_TYPE] = suggest_my_type
   ```

3. أضف `templates/my_type.md` (قالب Jinja2) يحتوي على تعليمات وبارامترات للوكيل.

4. أضف صف في جدول "مرجع أنواع المستندات" بملف `docs/README.zh.md`.

## الأداء والموارد

- زمن الانتقال المعتاد لكل طلب: 2–15 ثانية (حسب عدد الصفحات وسرعة API)
- استخدام الذاكرة: قد يصل إلى 2–3× حجم الملف أثناء معالجة PDFs
- وضع الدفعات لا يتضمن توازيًا مدمجًا؛ غلّفه بـ multiprocessing إذا لزم الأمر

## الترخيص

MIT-0

## سجل الإصدارات

- v1.0.0 — الإصدار الأولي (2025-03-15)

---

**مشاكل؟** راجع مخرج `stderr` أو افتح issue على GitHub.