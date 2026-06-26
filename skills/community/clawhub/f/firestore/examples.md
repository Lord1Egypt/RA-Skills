# Firestore Examples

## Few-Shot Prompting Examples

All examples below follow this policy: present the full command and wait for explicit user approval before execution, including read-only operations.

### Example 1: Creating a new document

**User prompt:** "Create a user document with first_name John, last_name Doe, and is_active true in the users collection"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context to the user
2. Get the project ID from the output (e.g., `my-project`)
3. Construct the curl command:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)

   curl -X POST \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "fields": {
         "first_name": { "stringValue": "John" },
         "last_name": { "stringValue": "Doe" },
         "is_active": { "booleanValue": true }
       }
     }' \
     "https://firestore.googleapis.com/v1/projects/my-project/databases/(default)/documents/users"
   ```
4. Present the command to the user
5. **Wait for user approval** before executing (this is a create operation)

**Note:** When creating a document without specifying a `documentId` parameter in the URL, Firestore automatically generates a unique document ID. To create a document with a specific ID, append `?documentId=YOUR_ID` to the URL (see Example 5).

### Example 2: Querying documents with a filter

**User prompt:** "Find all users where first_name equals John"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context to the user
2. Get the project ID from the output
3. Construct the query curl command:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)

   curl -X POST \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "structuredQuery": {
         "from": [{"collectionId": "users"}],
         "where": {
           "fieldFilter": {
             "field": {"fieldPath": "first_name"},
             "op": "EQUAL",
             "value": {"stringValue": "John"}
           }
         }
       }
     }' \
     "https://firestore.googleapis.com/v1/projects/my-project/databases/(default)/documents:runQuery"
   ```
4. Present the command to the user
5. **Wait for user approval** before executing (this is a read operation)
6. Parse and present the results to the user

### Example 3: Updating specific fields in a document

**User prompt:** "Update the user document admin_test_01 to change last_name to Smith and set is_active to false"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context to the user
2. Get the project ID from the output
3. Construct the update curl command with updateMask:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)

   curl -X PATCH \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "fields": {
         "last_name": { "stringValue": "Smith" },
         "is_active": { "booleanValue": false }
       }
     }' \
     "https://firestore.googleapis.com/v1/projects/my-project/databases/(default)/documents/users/admin_test_01?updateMask.fieldPaths=last_name&updateMask.fieldPaths=is_active"
   ```
4. Present the command to the user
5. **Wait for user approval** before executing (this is an update operation)

### Example 4: Deleting a document

**User prompt:** "Delete the user document admin_test_01"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context to the user
2. Get the project ID from the output
3. Construct the delete curl command:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)

   curl -X DELETE \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     "https://firestore.googleapis.com/v1/projects/my-project/databases/(default)/documents/users/admin_test_01"
   ```
4. Present the command to the user
5. **Wait for user approval** before executing (this is a delete operation)

### Example 5: Creating a document with a specific ID

**User prompt:** "Create a settings document with ID app_config containing theme as dark and notifications enabled"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context to the user
2. Get the project ID from the output
3. Construct the curl command with documentId parameter:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)

   curl -X POST \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "fields": {
         "theme": { "stringValue": "dark" },
         "notifications": { "booleanValue": true }
       }
     }' \
     "https://firestore.googleapis.com/v1/projects/my-project/databases/(default)/documents/settings?documentId=app_config"
   ```
4. Present the command to the user
5. **Wait for user approval** before executing (this is a create operation)

## Common Query Operators

When constructing queries, use these operators in the `fieldFilter.op` field:

- `EQUAL` - Field equals value
- `NOT_EQUAL` - Field does not equal value
- `LESS_THAN` - Field is less than value
- `LESS_THAN_OR_EQUAL` - Field is less than or equal to value
- `GREATER_THAN` - Field is greater than value
- `GREATER_THAN_OR_EQUAL` - Field is greater than or equal to value
- `ARRAY_CONTAINS` - Array field contains value
- `IN` - Field value is in the provided array
- `ARRAY_CONTAINS_ANY` - Array field contains any of the provided values
