
import requests
import json
import base64

def send_engagelab_email(api_user, api_key, from_address, to_addresses, subject, html_content=None, text_content=None, preview_text=None, 
                         cc_addresses=None, bcc_addresses=None, reply_to_addresses=None, 
                         vars_data=None, dynamic_vars_data=None, label_id=None, label_name=None, 
                         headers=None, attachments=None, settings=None, custom_args=None, request_id=None,
                         data_center_url="https://email.api.engagelab.cc"): # Default to Singapore data center
    
    auth_string = f"{api_user}:{api_key}"
    encoded_auth = base64.b64encode(auth_string.encode(\'utf-8\')).decode(\'utf-8\')

    url = f"{data_center_url}/v1/mail/send"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"Basic {encoded_auth}"
    }

    body_content = {}
    if html_content:
        body_content["html"] = html_content
    if text_content:
        body_content["text"] = text_content
    if preview_text:
        body_content["preview_text"] = preview_text

    mail_body = {
        "subject": subject,
        "content": body_content
    }

    if cc_addresses:
        mail_body["cc"] = cc_addresses
    if bcc_addresses:
        mail_body["bcc"] = bcc_addresses
    if reply_to_addresses:
        mail_body["reply_to"] = reply_to_addresses
    if vars_data:
        mail_body["vars"] = vars_data
    if dynamic_vars_data:
        mail_body["dynamic_vars"] = dynamic_vars_data
    if label_id:
        mail_body["label_id"] = label_id
    elif label_name:
        mail_body["label_name"] = label_name
    if headers:
        mail_body["headers"] = headers
    if attachments:
        mail_body["attachments"] = attachments
    if settings:
        mail_body["settings"] = settings

    payload = {
        "from": from_address,
        "to": to_addresses,
        "body": mail_body
    }

    if custom_args:
        payload["custom_args"] = custom_args
    if request_id:
        payload["request_id"] = request_id

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")
        return None

if __name__ == \'__main__\':
    # Example Usage (replace with actual credentials and data)
    API_USER = "your_api_user"
    API_KEY = "your_api_key"
    FROM_ADDRESS = "EngageLab Team<support@mail.engagelab.com>"
    TO_ADDRESSES = ["recipient@example.com"]
    SUBJECT = "Test Email from EngageLab Skill"
    HTML_CONTENT = "<p>Hello <strong>World</strong>!</p>"
    TEXT_CONTENT = "Hello World!"

    # Simple email
    # result = send_engagelab_email(API_USER, API_KEY, FROM_ADDRESS, TO_ADDRESSES, SUBJECT, html_content=HTML_CONTENT)
    # print(result)

    # Email with variables
    # vars_example = {"name": ["John Doe"]}
    # subject_vars = "Welcome, %name%!"
    # html_content_vars = "<p>Dear %name%, welcome to our service!</p>"
    # result_vars = send_engagelab_email(API_USER, API_KEY, FROM_ADDRESS, TO_ADDRESSES, subject_vars, html_content=html_content_vars, vars_data=vars_example)
    # print(result_vars)

    # Email with attachment (example: a dummy text file)
    # try:
    #     with open("dummy.txt", "w") as f:
    #         f.write("This is a dummy attachment.")
    #     with open("dummy.txt", "rb") as f:
    #         attachment_content = base64.b64encode(f.read()).decode(\'utf-8\')
    #     attachments_example = [
    #         {
    #             "content": attachment_content,
    #             "filename": "dummy.txt",
    #             "type": "text/plain",
    #             "disposition": "attachment"
    #         }
    #     ]
    #     result_attachment = send_engagelab_email(API_USER, API_KEY, FROM_ADDRESS, TO_ADDRESSES, SUBJECT, html_content=HTML_CONTENT, attachments=attachments_example)
    #     print(result_attachment)
    # except Exception as e:
    #     print(f"Error creating or reading dummy file: {e}")

    # Email with sandbox mode enabled
    # settings_example = {"sandbox": True}
    # result_sandbox = send_engagelab_email(API_USER, API_KEY, FROM_ADDRESS, TO_ADDRESSES, SUBJECT, html_content=HTML_CONTENT, settings=settings_example)
    # print(result_sandbox)

    pass
