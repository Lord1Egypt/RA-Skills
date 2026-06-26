# BDJobs API Reference

## Inputs

- Resume source: plaintext or LaTeX.
- Profile file: `data/userDetails.json`.
- Auth file: `data/loggedInData.json`.

## Login flow

### Check username
- `POST https://gateway.bdjobs.com/bdjobs-auth-dev/api/Login/ChecKUsername`
- Payload:
```json
{"username":"<username>","purpose":"login"}
```
- Use `event.eventData[0].value.guidId` as `userData`.

### Login
- `POST https://gateway.bdjobs.com/bdjobs-auth-dev/api/Login/Login`
- Payload:
```json
{
  "userName":"<username>",
  "password":"<password>",
  "systemId":1,
  "userid":"",
  "otp":"",
  "isForOTP":false,
  "socialMediaName":"",
  "userData":"<guidId>",
  "socialMediaId":"",
  "socialMediaAutoIncrementId":0,
  "purpose":"login",
  "referPage":"",
  "version":""
}
```
- Save `token`, `refreshToken`, `encryptId`, `decodeId`.

## Search

### Job search
- `GET https://api.bdjobs.com/Jobs/api/JobSearch/GetJobSearch`
- Include all query params, even if empty.
- Use `keyword`, `isFresher`, `pg`, `ToggleJobs=true`, `isPro=0`.

## Details

### Job details
- `GET https://gateway.bdjobs.com/jobapply/api/JobSubsystem/Job-Details?jobId=<jobId>`

## Applied jobs history

### GetApplyPositionInfoV1
- `GET https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/GetApplyPositionInfoV1?UserGuid=<guidId>&Version=EN&PageNumber=<page>&NoOfRecordPerPage=<count>`
- Use `guidId` from `data/loggedInData.json` or `data/userDetails.json`.
- Refresh `data/appliedJobIds.json` from this endpoint before fresh searches.

## Apply check

### JobApply
- `GET https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/JobApply?jobID=<jobId>&formValue=<encryptId>`
- Retry login on 401.

## Apply

### JobApplyPost
- `POST https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/JobApplyPost`
- Use the previous response data for payload fields.
- `formValue` must be `encodeURIComponent(encryptId)`.
- Retry login on 401.

## Undo

### UndoJobApply
- `POST https://testmongo.bdjobs.com/job-apply/api/JobSubsystem/UndoJobApply?JobID=<jobId>&FormValue=<encodedFormValue>`
- Use `encodeURIComponent(encryptId)` for `FormValue`.
- Retry login on 401.
- On success, remove the job ID from `data/appliedJobIds.json`.

## Update expected salary

### UpdateExpectedSalary
- `PUT https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/UpdateExpectedSalary`
- Payload:
```json
{
  "userGuid": "<guidId>",
  "jobId": <jobId>,
  "newSalary": <salary>
}
```
- Retry login on 401.
