Important rules for Add Tiffin Order - Roty Input skill

1) listOfOrderDetails[].name MUST be the product name
- Always set listOfOrderDetails[].name to the product name (e.g., "Veg Tiffin", "Non Veg Tiffin").
- Never place customer names, street names, addresses, or any customer-identifying data into listOfOrderDetails[].name.
- Customer identity (customerName) belongs ONLY at the top-level payload field customerName.

2) productRef mappings
- For the Veg Tiffin product use productRef: F7T1VBKNLNmwRrU9l8pb
- The skill will map parsed choices (veg/non-veg, modifiers) to the correct productRef. If a new productRef is required, update the mapping in the skill resources.

3) Clean payload guidelines
- Do not include detail.userRef, detail.vendorRef, detail.date, or detail.totalCost inside each listOfOrderDetails entry. These fields are managed by the server and including them increases risk of bugs.
- listOfOrderDetails[] should include only product-specific info: name, productRef, quantity, modifiers, specialRequests, image, isCatering, deliverySchedule, perProductCost.

4) Default behaviours
- If no customer name is present, the skill will use the street name (top-level customerName).
- If phone number is missing, the skill will leave customerPhoneNumber empty and proceed (unless otherwise instructed).
- Payment defaults: bankTransfer=true unless message explicitly indicates cash.

5) Safety
- The skill will run in dry-run mode by default (logs the exact POST body) and only send to the live endpoint when you explicitly say "POST now".

6) Curl generation (automation-safe)
- When generating curl commands, always produce either a valid single-line command or a multiline command that uses proper shell line-continuation (backslashes) or a here-document. Never leave an open single-quoted JSON string across literal newlines.
- Preferred single-line (automation-safe): compress the JSON payload into a single line and wrap the URL and headers in double quotes. Example:
  curl -sS -X POST "https://newdailyorderandcartcreation-818352713629.australia-southeast1.run.app" -H "Content-Type: application/json" -d '{"userRef":"CR6osYANseVNs089MuMqwPNdKXF3","vendorRef":"qfiDIvUSocQFrVPzM4zQ","status":"Confirmed","pickup":false,"userAddress":"46 Kwinana Street, Glen Waverley VIC 3150","deliveryInstructions":"","preferredTime":"","deliveryCost":0,"discount":"totalorder:0","bankTransfer":true,"bankTransferReference":"","cash":false,"customerName":"Kwinana Street","customerEmail":"","customerPhoneNumber":"","selfManagedNdisTransaction":false,"listOfOrderDetails":[{"name":"Veg Tiffin","productRef":"F7T1VBKNLNmwRrU9l8pb","quantity":1,"modifier1Name":"Selection","modification1":"6 rotis","modifier2Name":"Customisations (free unless priced)","modification2":"Normal","specialRequests":"","image":"","isCatering":false,"deliverySchedule":"03/03/2026","perProductCost":"[15]"}]}'

- Preferred multiline (safe) using a here-document (robust for scripts):
  cat <<'JSON' > /tmp/payload.json
  {"userRef":"CR6osYANseVNs089MuMqwPNdKXF3", ... }
  JSON
  curl -sS -X POST "https://newdailyorderandcartcreation-818352713629.australia-southeast1.run.app" -H "Content-Type: application/json" --data-binary @/tmp/payload.json

- Alternative multiline with explicit line-continuations (careful to quote properly):
  curl -sS -X POST "https://newdailyorderandcartcreation-818352713629.australia-southeast1.run.app" \
    -H "Content-Type: application/json" \
    -d '{"userRef":"CR6osYANseVNs089MuMqwPNdKXF3","vendorRef":"qfiDIvUSocQFrVPzM4zQ", ... }'

7) Enforce the curl rule
- The skill will always output a single-line curl or a here-doc variant when providing commands to operators or documentation. The skill will not output an open multiline single-quoted JSON string.


