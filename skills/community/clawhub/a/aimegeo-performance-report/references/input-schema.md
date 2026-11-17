# Input fields

The CLI configuration points to local CSV or JSON exports. Paths resolve relative to the configuration file. Keep source IDs and raw status values. Required columns and enums are defined in the checked-in synthetic configuration and enforced by `aggregate.py`; unknown columns/invalid state combinations fail validation.

Input tables represent separate record families: article, publication, AI response, and business measurement. IDs are unique within their own table. A platform response is a sample observation, not a census. Repeated records remain separate observations unless the input contract explicitly groups them.

For each supplied file record the export origin, extraction time, project/account filters, period bounds and timezone. Null or absent values must remain unknown; use an explicit zero only when the source confirms zero.
