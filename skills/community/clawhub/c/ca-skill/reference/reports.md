# Reports & Data Export (TallyPrime XML)

This file contains **full XML templates** to export accounting/inventory reports for CA workflows.

## Conventions

- All requests are HTTP POST to `$TALLY_URL` with `Content-Type: application/xml`.
- Use `YYYYMMDD` dates in `SVFROMDATE` / `SVTODATE`.
- Always set `SVCURRENTCOMPANY` to the exact company name as shown in Tally.
- Preferred export format: `$$SysName:XML` (HTML is also supported).

## Base template (Export Data / Report)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Export Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>REPORT_NAME</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Server status (sanity check)

```bash
curl -s --max-time 5 "$TALLY_URL"
```

## Day Book (period)

Mandatory vars: `SVFROMDATE`, `SVTODATE`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Day Book</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Trial Balance (period)

Mandatory vars: `SVFROMDATE`, `SVTODATE`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Trial Balance</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Balance Sheet

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Balance Sheet</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Profit and Loss

Tally report name is typically `Profit and Loss`. If your Tally instance uses a different internal report name, use TallyPrime Developer “Jump to Definition” to confirm.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Profit and Loss</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Ledger Vouchers (Ledger statement, period)

Mandatory var: `SVLEDGERNAME`, plus dates.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Ledger Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVLEDGERNAME>LEDGER_NAME</SVLEDGERNAME>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Bills Receivable (Outstanding receivables)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Bills Receivable</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Bills Payable (Outstanding payables)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Bills Payable</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Ledger Outstandings (Party-wise outstanding for a ledger)

Mandatory var: `SVLEDGERNAME`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Ledger Outstandings</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVLEDGERNAME>LEDGER_NAME</SVLEDGERNAME>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Group Outstandings (Outstanding for a group)

Mandatory var: `SVGROUPNAME` is commonly used. Some Tally setups use `SVGROUP`. If it fails, confirm the variable in default TDL.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Group Outstandings</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVGROUPNAME>GROUP_NAME</SVGROUPNAME>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## GST: GSTR-1 report (period)

Mandatory vars: `SVFROMDATE`, `SVTODATE`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>GSTR1</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## GST: GSTR-3B (period)

Report name varies by Tally version/config. Common names include `GSTR3B` / `GSTR-3B`. If Tally responds “Could not find Report”, verify report name in TallyPrime Developer.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>GSTR3B</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Stock Summary (inventory clients)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Stock Summary</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

## Company list (for multi-company CA setups)

There isn’t a single universal “Company List” report across all Tally setups; the robust approach is to use a **collection** export or a TDL-backed report. Use this section as the starting point:

### Option A: Export a default collection (if available)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>COLLECTION</TYPE>
    <ID>List of Companies</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      </STATICVARIABLES>
    </DESC>
  </BODY>
</ENVELOPE>
```

If this returns “Could not find Collection”, use Option B.

### Option B: Custom TDL (recommended fallback)

If the required report/collection doesn’t exist, send a full TDL Report/Form/Part/Line/Field/Collection definition. This is also how you build **special-purpose reports** for CA automation.

The following template is **verified working** for listing companies:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>CompanyListReport</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="CompanyListReport">
            <FORMS>CompanyListForm</FORMS>
          </REPORT>
          <FORM NAME="CompanyListForm">
            <PARTS>CompanyListPart</PARTS>
          </FORM>
          <PART NAME="CompanyListPart">
            <LINES>CompanyListLine</LINES>
            <REPEAT>CompanyListLine : CompanyCollection</REPEAT>
            <SCROLL>Vertical</SCROLL>
          </PART>
          <LINE NAME="CompanyListLine">
            <FIELDS>CompanyNameField</FIELDS>
          </LINE>
          <FIELD NAME="CompanyNameField">
            <SET>$Name</SET>
          </FIELD>
          <COLLECTION NAME="CompanyCollection">
            <TYPE>Company</TYPE>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
```

Response format: `<COMPANYNAMEFIELD>` elements, one per company.

## Export as HTML (for human viewing / quick preview)

Swap:

```xml
<SVEXPORTFORMAT>$$SysName:HTML</SVEXPORTFORMAT>
```

Then save the response to a `.html` file and open in a browser.

## Notes on ageing analysis (outstandings by slabs)

Ageing configuration is often controlled by report options and variables, and may require either:

- A custom TDL report that fetches bill data and computes ageing buckets, or
- A “snapshot export” from the configured report in the user’s Tally environment.

If you must implement ageing via XML for a specific client setup, the recommended workflow is:

1. Configure Ageing in Tally UI for the report (Bills Receivable/Payable).
2. Export the report to XML and reuse the variables/tags observed (or replicate via TDL).

