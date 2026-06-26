# Custom Fields API Reference

Custom fields in AC are split into definitions (schema) and values (data). Contact fields and deal fields use different endpoints.

## Contact custom fields

### List field definitions

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/fields" | jq
```

Returns field `id`, `title`, `type`, and `options` (for dropdowns, `||`-delimited).

Field types: `text`, `textarea`, `date`, `datetime`, `dropdown`, `multiselect`, `radio`, `checkbox`, `listbox`, `hidden`, `number`.

### Read field values for a contact

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/{contactId}/fieldValues" | jq
```

Returns `fieldValues` array. Each has `field` (field ID), `value`, and `contact` (contact ID).

### Write a field value

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fieldValue":{"contact":"123","field":"7","value":"Enterprise"}}' \
  "$AC_API_URL/api/3/fieldValues" | jq
```

To update, use `PUT` with the fieldValue ID:

```bash
curl -s -X PUT -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fieldValue":{"contact":"123","field":"7","value":"Pro"}}' \
  "$AC_API_URL/api/3/fieldValues/{fieldValueId}" | jq
```

### Create a new field definition

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field":{"title":"Signup Source","type":"dropdown","options":"Organic||Paid||Referral"}}' \
  "$AC_API_URL/api/3/fields" | jq
```

## Deal custom fields

### List deal field definitions

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealCustomFieldMeta" | jq
```

### Read deal field values

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealCustomFieldData?filters[dealId]={dealId}" | jq
```

### Write a deal field value

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dealCustomFieldDatum":{"dealId":"45","customFieldId":"1","fieldValue":"250000"}}' \
  "$AC_API_URL/api/3/dealCustomFieldData" | jq
```

### Create a deal field definition

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dealCustomFieldMetum":{"fieldLabel":"Renewal Date","fieldType":"date"}}' \
  "$AC_API_URL/api/3/dealCustomFieldMeta" | jq
```

Deal field types: `text`, `textarea`, `date`, `datetime`, `dropdown`, `multiselect`, `radio`, `checkbox`, `listbox`, `hidden`, `currency`, `number`.

## Multi-value fields

Dropdown and multiselect options use `||` as delimiter:

```
"options": "red||blue||green"
```

When writing a multiselect value, also use `||`:

```json
{"fieldValue": {"contact": "123", "field": "9", "value": "red||blue"}}
```

## Using field values with contact/sync

You can set field values directly during contact sync using the `fieldValues` array:

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "email": "jane@example.com",
      "firstName": "Jane",
      "fieldValues": [
        {"field": "1", "value": "Enterprise"},
        {"field": "3", "value": "2026-04-24"}
      ]
    }
  }' \
  "$AC_API_URL/api/3/contact/sync" | jq
```

## Gotchas

- **Field values are NOT on the contact object.** You must query `fieldValues` separately or use the `?include=fieldValues` parameter on contact retrieval.
- **Field IDs in `state.json`.** Always look up the field ID from the taxonomy before writing. Don't guess — field IDs are account-specific.
- **Date format** for date fields: `YYYY-MM-DD`.
- **Currency fields** store values as strings, not integers.
- **NEVER delete a field definition without explicit user confirmation.** Deleting a field definition destroys ALL associated values across every contact or deal in the account. This is irreversible. There is no undo. Always warn the user of the blast radius before proceeding.
