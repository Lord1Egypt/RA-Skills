# Firestore Troubleshooting

## 401 Unauthorized

- Token expired. Regenerate with:
  ```bash
  ACCESS_TOKEN=$(gcloud auth print-access-token)
  ```
- Incorrect authentication. Re-authenticate:
  ```bash
  gcloud auth login
  ```
- Validate active account and project:
  ```bash
  gcloud config list --format='text(core.account,core.project)'
  ```

## 403 Forbidden

- Insufficient IAM permissions for the authenticated identity.
- Firestore API is not enabled in the target project.
- Verify role assignment and project context before retrying.

## 404 Not Found

- Incorrect project ID, database ID, collection path, or document path.
- Requested collection or document does not exist.
- Confirm the endpoint path format:
  ```text
  /v1/projects/{PROJECT_ID}/databases/{DATABASE_ID}/documents/{COLLECTION}/{DOCUMENT_ID}
  ```

## 400 Bad Request

- Invalid JSON payload format.
- Invalid Firestore field types (for example, using `stringValue` where `integerValue` is expected).
- Missing required request body fields.
- Incorrect query structure for `documents:runQuery`.

## Update Errors

- Missing `updateMask.fieldPaths` when partially updating documents.
- Updating a path that does not exist.
- Using invalid field path names in update masks.

## Quick Debug Checklist

1. Confirm active context:
   ```bash
   gcloud config list --format='text(core.account,core.project)'
   ```
2. Refresh token:
   ```bash
   ACCESS_TOKEN=$(gcloud auth print-access-token)
   ```
3. Test API reachability with a simple read request.
4. Validate JSON payload with a linter before sending.
5. Recheck IAM roles and Firestore API enablement.
