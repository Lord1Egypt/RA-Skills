package client

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type APIClient struct {
	SecretID  string
	SecretKey string
	Region    string
	Endpoint  string
	Service   string
	Version   string
	Client    *http.Client
}

func NewAPIClient(secretID, secretKey, region, endpoint string) *APIClient {
	if endpoint == "" {
		endpoint = "cls.tencentcloudapi.com"
	}
	return &APIClient{
		SecretID:  secretID,
		SecretKey: secretKey,
		Region:    region,
		Endpoint:  endpoint,
		Service:   "cls",
		Version:   "2020-10-16",
		Client:    &http.Client{Timeout: 30 * time.Second},
	}
}

// Call makes a CLS API call with TC3-HMAC-SHA256 signing.
func (c *APIClient) Call(action string, params map[string]interface{}) (map[string]interface{}, error) {
	payload, err := json.Marshal(params)
	if err != nil {
		return nil, fmt.Errorf("序列化请求参数失败: %w", err)
	}

	timestamp := time.Now().Unix()
	date := time.Unix(timestamp, 0).UTC().Format("2006-01-02")

	// Build canonical request
	hashedPayload := sha256Hex(payload)
	canonicalRequest := fmt.Sprintf("POST\n/\n\ncontent-type:application/json\nhost:%s\n\ncontent-type;host\n%s",
		c.Endpoint, hashedPayload)

	// Build string to sign
	credentialScope := fmt.Sprintf("%s/%s/tc3_request", date, c.Service)
	stringToSign := fmt.Sprintf("TC3-HMAC-SHA256\n%d\n%s\n%s",
		timestamp, credentialScope, sha256Hex([]byte(canonicalRequest)))

	// Calculate signature
	secretDate := hmacSHA256([]byte("TC3"+c.SecretKey), []byte(date))
	secretService := hmacSHA256(secretDate, []byte(c.Service))
	secretSigning := hmacSHA256(secretService, []byte("tc3_request"))
	signature := hex.EncodeToString(hmacSHA256(secretSigning, []byte(stringToSign)))

	// Build authorization header
	authorization := fmt.Sprintf("TC3-HMAC-SHA256 Credential=%s/%s, SignedHeaders=content-type;host, Signature=%s",
		c.SecretID, credentialScope, signature)

	// Build request
	url := fmt.Sprintf("https://%s", c.Endpoint)
	req, err := http.NewRequest("POST", url, bytes.NewReader(payload))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Host", c.Endpoint)
	req.Header.Set("Authorization", authorization)
	req.Header.Set("X-TC-Action", action)
	req.Header.Set("X-TC-Version", c.Version)
	req.Header.Set("X-TC-Timestamp", fmt.Sprintf("%d", timestamp))
	req.Header.Set("X-TC-Region", c.Region)

	// Send request
	resp, err := c.Client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("API 请求失败: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("读取响应失败: %w", err)
	}

	// Parse response
	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("解析响应失败: %w\n响应内容: %s", err, string(body))
	}

	// Check for API error
	if response, ok := result["Response"].(map[string]interface{}); ok {
		if errObj, ok := response["Error"].(map[string]interface{}); ok {
			code, _ := errObj["Code"].(string)
			message, _ := errObj["Message"].(string)
			requestID, _ := response["RequestId"].(string)
			return nil, fmt.Errorf("[%s] %s (RequestId: %s)", code, message, requestID)
		}
	}

	return result, nil
}

// CallRaw returns the raw JSON string response.
func (c *APIClient) CallRaw(action string, paramsJSON string) (string, error) {
	var params map[string]interface{}
	if paramsJSON == "" || paramsJSON == "{}" {
		params = make(map[string]interface{})
	} else {
		if err := json.Unmarshal([]byte(paramsJSON), &params); err != nil {
			return "", fmt.Errorf("参数 JSON 解析失败: %w", err)
		}
	}

	result, err := c.Call(action, params)
	if err != nil {
		return "", err
	}

	b, err := json.Marshal(result)
	if err != nil {
		return "", err
	}
	return string(b), nil
}

func sha256Hex(data []byte) string {
	h := sha256.New()
	h.Write(data)
	return hex.EncodeToString(h.Sum(nil))
}

func hmacSHA256(key, data []byte) []byte {
	h := hmac.New(sha256.New, key)
	h.Write(data)
	return h.Sum(nil)
}
