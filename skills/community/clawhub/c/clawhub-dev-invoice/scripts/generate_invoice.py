#!/usr/bin/env python3
&quot;&quot;&quot;
Generate HTML invoice from JSON input for ClawHub dev services.
Usage: python scripts/generate_invoice.py input.json
Outputs: invoice_XXXX.html (convert to PDF with pandoc/wkhtmltopdf/browser)
&quot;&quot;&quot;

import sys
import json

def main():
    if len(sys.argv) != 2:
        print(&quot;Usage: python generate_invoice.py &lt;input.json&gt;&quot;)
        sys.exit(1)

    try:
        with open(sys.argv[1], &#39;r&#39;) as f:
            data = json.load(f)
    except Exception as e:
        print(f&quot;Error loading JSON: {e}&quot;)
        sys.exit(1)

    # Calculate subtotals
    subtotal = 0.0
    expenses = data.get(&#39;expenses&#39;, 0.0)
    items = data[&#39;items&#39;]

    for item in items:
        if &#39;hours&#39; in item and &#39;rate&#39; in item:
            amount = item[&#39;hours&#39;] * item[&#39;rate&#39;]
        elif &#39;fixed&#39; in item:
            amount = float(item[&#39;fixed&#39;])
        else:
            amount = 0.0
        item[&#39;amount&#39;] = amount
        subtotal += amount

    subtotal += expenses  # Expenses before tax
    gst = subtotal * 0.05
    total = subtotal + gst

    # Generate HTML
    html = f&quot;&quot;&quot;
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Invoice {data[&#39;invoice_num&#39;]}&lt;/title&gt;
    &lt;style&gt;
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .total {{ font-weight: bold; font-size: 1.2em; }}
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Invoice #{data[&#39;invoice_num&#39;]}&lt;/h1&gt;
    &lt;p&gt;&lt;strong&gt;Date:&lt;/strong&gt; {data[&#39;date&#39;]} | &lt;strong&gt;Due:&lt;/strong&gt; {data[&#39;due_date&#39;]}&lt;/p&gt;

    &lt;h2&gt;Bill To:&lt;/h2&gt;
    &lt;p&gt;{data[&#39;client&#39;][&#39;name&#39;]}&lt;br&gt;
    {data[&#39;client&#39;][&#39;address&#39;]}&lt;br&gt;
    {data[&#39;client&#39;][&#39;email&#39;]}&lt;/p&gt;

    &lt;h2&gt;From:&lt;/h2&gt;
    &lt;p&gt;Thomas&lt;br&gt;
    Clavet, Saskatchewan, Canada&lt;br&gt;
    thomas@openclaw.ai&lt;/p&gt;

    &lt;table&gt;
        &lt;tr&gt;&lt;th&gt;Description&lt;/th&gt;&lt;th&gt;Hours/Qty&lt;/th&gt;&lt;th&gt;Rate&lt;/th&gt;&lt;th&gt;Amount (CAD)&lt;/th&gt;&lt;/tr&gt;
&quot;&quot;&quot;

    for item in items:
        qty = item.get(&#39;hours&#39;, item.get(&#39;fixed&#39;, &#39;&#39;))
        rate = item.get(&#39;rate&#39;, &#39;Fixed&#39;)
        html += f&quot;        &lt;tr&gt;&lt;td&gt;{{item[&#39;desc&#39;]}}&lt;/td&gt;&lt;td&gt;{{qty}}&lt;/td&gt;&lt;td&gt;${{rate}}&lt;/td&gt;&lt;td&gt;${{item[&#39;amount&#39;]:.2f}}&lt;/td&gt;&lt;/tr&gt;\n&quot;

    if expenses:
        html += f&quot;        &lt;tr&gt;&lt;td&gt;Expenses&lt;/td&gt;&lt;td&gt;&lt;/td&gt;&lt;td&gt;&lt;/td&gt;&lt;td&gt;${{expenses:.2f}}&lt;/td&gt;&lt;/tr&gt;\n&quot;

    html += f&quot;&quot;&quot;
    &lt;/table&gt;
    &lt;p&gt;&lt;strong&gt;Subtotal:&lt;/strong&gt; ${subtotal:.2f}&lt;/p&gt;
    &lt;p&gt;&lt;strong&gt;GST (5%):&lt;/strong&gt; ${gst:.2f}&lt;/p&gt;
    &lt;p class=&quot;total&quot;&gt;&lt;strong&gt;Total Due: ${total:.2f} CAD&lt;/strong&gt;&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
&quot;&quot;&quot;

    output_file = f&quot;invoice_{{data[&#39;invoice_num&#39;]}}.html&quot;
    with open(output_file, &#39;w&#39;) as f:
        f.write(html)
    print(f&quot;Generated {{output_file}}&quot;)
    print(&quot;To create PDF: Use browser pdf tool or exec &#39;wkhtmltopdf {{output_file}} {{output_file.replace(&#39;.html&#39;, &#39;.pdf&#39;)}}&#39; if installed.&quot;)

if __name__ == &quot;__main__&quot;
    main()
