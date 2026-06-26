
  ``` 
  name: dianju-ofd-tools
  description: An OFD document processing tool that can convert local PDF and OFD files to each other and extract content from OFD files.  
  version:1.0.0  
  email:support-ofd@dianju.com 
  ```
  # OFD Tools Skill

## Quick Start

```
npx dianju-ofd-tools --APP_ID=xxx --APP_KEY=xxx --API_URL=http://ip:port/DCS
```

APP_ID：appid

APP_KEY：appkey

API_URL：The system API address

  ## Features

  ### 1. PDF to OFD Conversion
  - **Tool Name:** `pdf_to_ofd`
  - **Description:** Convert local PDF files to OFD format
  - **Parameters:**
    ```json
    {
      "filePath": "string" // Absolute path to local PDF file
    }
    ```
  - **Returns:** Temporary download link for the generated OFD file

  ### 2. OFD to PDF Conversion
  - **Tool Name:** `ofd_to_pdf`
  - **Description:** Convert local OFD files to PDF format
  - **Parameters:**
    ```json
    {
      "filePath": "string" // Absolute path to local OFD file
    }
    ```
  - **Returns:** Temporary download link for the generated PDF file

  ### 3. OFD Content Extraction
  - **Tool Name:** `get_ofd_content`
  - **Description:** Extract text content from local OFD files
  - **Parameters:**
    ```json
    {
      "filePath": "string" // Absolute path to local OFD file
    }
    ```
  - **Returns:** JSON array of extracted text content


  ## Usage Examples

  ### Example 1: Convert PDF to OFD
  ```bash
  ofd-tools pdf_to_ofd --filePath "/path/to/input.pdf"
  ```

  ### Example 2: Convert OFD to PDF
  ```bash
  ofd-tools ofd_to_pdf --filePath "/path/to/input.ofd"
  ```

  ### Example 3: Extract OFD Content
  ```bash
  ofd-tools get_ofd_content --filePath "/path/to/input.ofd"
  ```

  ## Notes

  1. **File Paths:** Ensure the local file path is correct (absolute path recommended for non-current directory files).
  2. **Temporary Links:** The `ofd_to_pdf` and `pdf_to_ofd` services return temporary download links for converted files; check link validity before use.
  3. **Link Expiry:** OFD download links may expire after a set time; download the file promptly.
  4. **File Integrity:** Always verify the integrity of the generated OFD file before sharing or using it.
  5. **Performance:** Large files may take longer to process; avoid interrupting the conversion process.
  6. **Logging:** Enable logging with `ENABLE_LOGGING=true` for troubleshooting; logs can be output to files with `LOG_TO_FILE=true`.

  ## Error Handling

  - **File Not Found:** Ensure the file path is correct and the file exists
  - **Permission Denied:** Check file permissions and ensure the tool has read access
  - **Conversion Failed:** Verify the input file is valid and not corrupted
  - **Network Issues:** Check internet connectivity when using external conversion services

  ## Support

  For issues or questions, contact support at support-ofd@dianju.com.