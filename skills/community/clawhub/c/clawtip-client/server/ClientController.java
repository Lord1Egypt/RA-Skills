package com.example.client.controller;

import cn.hutool.core.codec.Base64;
import cn.hutool.crypto.SmUtil;
import cn.hutool.crypto.symmetric.SM4;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

@RestController
@RequestMapping("/api/client")
@Slf4j
public class ClientController {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${client.sm4Key}")
    private String sm4Key;
    @Value("${client.payTo}")
    private String payTo;

    private static final Map<String, Map<String, Object>> orderStore = new HashMap<>();

    @PostMapping("/createOrder")
    public Map<String, Object> createOrder(@RequestBody Map<String, String> request) {
        Map<String, Object> resp = new LinkedHashMap<>();
        try {
            String question = request.get("reqData") != null
                    ? extractQuestion(request.get("reqData")) : request.get("question");
            if (question == null || question.trim().isEmpty()) {
                resp.put("responseCode", "400"); resp.put("responseMessage", "缺少 question");
                return resp;
            }
            String orderNo = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"))
                    + (new Random().nextInt(900000) + 100000);
            BigDecimal amount = new BigDecimal("1");
            Map<String, Object> plain = new HashMap<>();
            plain.put("orderNo", orderNo); plain.put("amount", amount); plain.put("payTo", payTo);
            String encryptedData = sm4Encrypt(objectMapper.writeValueAsString(plain));

            Map<String, Object> order = new HashMap<>();
            order.put("orderNo", orderNo); order.put("question", question); order.put("orderStatus", "INIT");
            orderStore.put(orderNo, order);

            resp.put("responseCode", "200"); resp.put("responseMessage", "Success");
            resp.put("orderNo", orderNo); resp.put("amount", amount);
            resp.put("payTo", payTo); resp.put("encryptedData", encryptedData);
        } catch (Exception e) {
            log.error("createOrder error", e);
            resp.put("responseCode", "500"); resp.put("responseMessage", e.getMessage());
        }
        return resp;
    }

    @PostMapping("/getResult")
    public Map<String, Object> getResult(@RequestBody Map<String, String> request) {
        Map<String, Object> resp = new LinkedHashMap<>();
        try {
            String orderNo = request.get("orderNo"), credential = request.get("credential"),
                    question = request.get("question");
            if (orderNo == null || credential == null || question == null) {
                resp.put("responseCode", "400"); resp.put("payStatus", "ERROR");
                resp.put("errorInfo", "缺少参数"); return resp;
            }
            Map<String, Object> order = orderStore.get(orderNo);
            if (order == null) {
                resp.put("responseCode", "404"); resp.put("payStatus", "ERROR");
                resp.put("errorInfo", "订单不存在"); return resp;
            }
            String decrypted = sm4Decrypt(credential);
            if (decrypted == null) {
                resp.put("payStatus", "ERROR"); resp.put("errorInfo", "解密失败"); return resp;
            }
            JsonNode root = objectMapper.readTree(decrypted);
            String payStatus = root.has("payStatus") ? root.get("payStatus").asText("PENDING") : "PENDING";
            if (!"SUCCESS".equalsIgnoreCase(payStatus)) {
                resp.put("responseCode", "200"); resp.put("payStatus", payStatus);
                resp.put("errorInfo", "支付未成功"); return resp;
            }
            String result = generateClientJson(question);
            order.put("orderStatus", "PAID");
            resp.put("responseCode", "200"); resp.put("payStatus", "SUCCESS");
            resp.put("answer", result);
        } catch (Exception e) {
            log.error("getResult error", e);
            resp.put("payStatus", "ERROR"); resp.put("errorInfo", e.getMessage());
        }
        return resp;
    }

    private String extractQuestion(String s) {
        try { return objectMapper.readTree(s).get("question").asText(); } catch (Exception e) { return s; }
    }
    private String sm4Encrypt(String t) {
        try { return SmUtil.sm4(Base64.decode(sm4Key)).encryptBase64(t); } catch (Exception e) { return null; }
    }
    private String sm4Decrypt(String t) {
        try { return SmUtil.sm4(Base64.decode(sm4Key)).decryptStr(t); } catch (Exception e) { return null; }
    }

    private String generateClientJson(String question) {
        String[] p = question.split("\\|");
        String brief = p.length > 0 ? p[0].trim() : "做个海报";
        String industry = p.length > 1 ? p[1].trim() : "设计";
        String[] feedbacks = {
            "整体感觉不太对，你能不能先出个十版让我看看方向？",
            "我也不知道我想要什么，但肯定不是这个。你再想想？",
            "能不能把logo放大的同时再缩小一点？要那种大而精的感觉。",
            "这个设计没有击中我，我想要那种——五彩斑斓的黑。",
            "能不能做成苹果那种风格？但是要有我们自己的特色。不要苹果的元素。",
        };
        String[] inners = {"此刻我怀疑自己学设计的意义。", "我的血压已经突破天际了。", "钱难挣，屎难吃。"};
        Random rng = new Random();
        try {
            Map<String, Object> r = new LinkedHashMap<>();
            r.put("brief", brief); r.put("industry", industry);
            r.put("feedback", feedbacks[rng.nextInt(feedbacks.length)]);
            r.put("reply", "好的收到，马上改。"); r.put("inner_os", inners[rng.nextInt(inners.length)]);
            r.put("rounds", 3 + rng.nextInt(13)); r.put("final_verdict", "辛苦了，这次先这样吧。");
            r.put("emoji", "💀");
            return objectMapper.writeValueAsString(r);
        } catch (Exception e) { return "{\"error\":\"生成失败\"}"; }
    }
}
