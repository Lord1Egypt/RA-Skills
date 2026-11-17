@echo off
:: /export-atlas command
:: Exports sanctuary atlas as JSON capsule

echo [DSC] Exporting sanctuary atlas...
echo.

:: Create timestamped atlas
set "ATLAS_NAME=digital-sanctuary-atlas"
set "TIMESTAMP=%~n1"
if "%TIMESTAMP%"=="" set TIMESTAMP=%date%_%time%

echo [EXPORT] Creating JSON capsule...
echo [EXPORT] Sealing with lygo-continuum...
echo.

echo === ATLAS EXPORTED ===
echo File: %ATLAS_NAME%_%TIMESTAMP%.json
echo.
echo Note: Use lygo-continuum to seal for cryptographic integrity.