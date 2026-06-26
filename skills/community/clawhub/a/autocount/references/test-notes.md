# AutoCount Invoice Test Notes

## Environment observed

- Base URL shape: `http://your-autocount-host:9999`
- Protocol in the tested environment: HTTP on 9999, not HTTPS
- Root path returned `404 Not Found`
- Server header observed in testing: `Microsoft-HTTPAPI/2.0`

## Auth behavior

- Basic auth failed
- `APIKey`, `ApiKey` headers did not work
- `X-API-KEY` triggered the next auth layer
- Missing companion header error showed `X-API-Name is required`
- Working auth shape:
  - `X-API-NAME: <your-api-name>`
  - `X-API-KEY: <your-api-key>`

## Sales-side endpoints verified

- `POST /api/Invoice/CreateRecord`
- `GET /api/Invoice/GetRecord?docKey=<docKey>`

## Purchase-side endpoints verified

- `POST /api/PurchaseOrder/GetRecordList` with `{}`
- `GET /api/PurchaseOrder/GetRecord?docKey=<docKey>`
- `POST /api/GoodsReceivedNote/GetRecordList` with `{}`
- `GET /api/GoodsReceivedNote/GetRecord?docKey=<docKey>`
- `POST /api/GoodsReceivedNote/CreateRecord`
- `POST /api/PurchaseInvoice/CreateRecord`

## Master-data endpoints observed

- `/api/Debtor/GetRecordList`
- `/api/Creditor/GetRecordList`
- `/api/Item/GetRecordList`
- `/api/Location/GetRecordList`
- `/api/Currency/GetRecordList`

## Live create results

### Sales invoices
- Sales invoice creation worked repeatedly in live testing
- Fetch after create returned a valid invoice number
- Enriched invoice creation also worked
- `TaxCode: "<<<Default>>>"` worked

### GRN
- First GRN create attempt failed because `DocNo` was missing
- Error: `Column 'DocNo' does not allow nulls.`
- Adding `DocNo: "<<<Default>>>"` fixed it
- GRN creation then worked

### Purchase invoice
- Purchase invoice creation worked

## Purchase chain observations

### Latest PO observed during testing
- A final PO with a creditor, item, qty, UOM, and unit price was successfully inspected and used for transfer testing

### Existing GRN observed for shape comparison
- An existing GRN including `SupplierDONo` helped confirm request body shape

## Working item patterns

### Item `00001`
- Description: `FABRIC`
- UOM: `METER`
- Origin country used successfully: `MYS`
- Repeatedly created sales invoices successfully

### Item `00058`
- Earlier successful in a richer payload
- In one simplified batch, failed with:
  - `Origin Country Code Not Found ()`
- Conclusion: some items require more careful field population

## Important behavior notes

- Small payloads may create technically valid documents but leave UI-facing display fields blank
- Enriching from master data before create gives better results
- Do not blindly hardcode tax code values
- Prefer `<<<Default>>>` where the API supports it
- Prefer draft creation during tests
- `PurchaseOrder/GetRecordList` and `GoodsReceivedNote/GetRecordList` are POST endpoints, not GET
