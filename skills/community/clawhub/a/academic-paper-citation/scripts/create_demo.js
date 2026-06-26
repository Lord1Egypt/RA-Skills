const { Document, Packer, Paragraph, TextRun, Footer, PageNumber, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');

// 创建一个带引用编号的示例Word文档
const doc = new Document({
    sections: [{
        properties: {
            page: {
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        children: [
            // 标题
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "引用编号演示文档", bold: true, size: 36 })]
            }),
            new Paragraph({ children: [new TextRun("")] }), // 空行
            
            // 正文段落
            new Paragraph({
                children: [
                    new TextRun({ text: "这是一篇用于演示Word文档引用编号的示例文档。在学术写作中，正确引用参考文献是非常重要的。", size: 24 })
                ]
            }),
            new Paragraph({ children: [new TextRun("")] }),
            
            // 带引用的段落 - 使用上标格式模拟引用编号
            new Paragraph({
                children: [
                    new TextRun({ text: "深度学习在自然语言处理领域取得了显著进展", size: 24 }),
                    new TextRun({ text: "[1]", superScript: true, size: 20 }),
                    new TextRun({ text: "。Transformer架构的提出彻底改变了这一领域", size: 24 }),
                    new TextRun({ text: "[2]", superScript: true, size: 20 }),
                    new TextRun({ text: "。", size: 24 })
                ]
            }),
            new Paragraph({ children: [new TextRun("")] }),
            
            new Paragraph({
                children: [
                    new TextRun({ text: "注意力机制允许模型在处理序列时关注不同位置的信息", size: 24 }),
                    new TextRun({ text: "[3]", superScript: true, size: 20 }),
                    new TextRun({ text: "。这一机制已被广泛应用于机器翻译、文本摘要等任务", size: 24 }),
                    new TextRun({ text: "[4,5]", superScript: true, size: 20 }),
                    new TextRun({ text: "。", size: 24 })
                ]
            }),
            new Paragraph({ children: [new TextRun("")] }),
            
            // 参考文献标题
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun({ text: "参考文献", bold: true, size: 32 })]
            }),
            new Paragraph({ children: [new TextRun("")] }),
            
            // 参考文献列表
            new Paragraph({
                children: [
                    new TextRun({ text: "[1] ", size: 22 }),
                    new TextRun({ text: "LeCun Y, Bengio Y, Hinton G. Deep learning. Nature, 2015, 521(7553): 436-444.", size: 22 })
                ]
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "[2] ", size: 22 }),
                    new TextRun({ text: "Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. NeurIPS, 2017: 5998-6008.", size: 22 })
                ]
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "[3] ", size: 22 }),
                    new TextRun({ text: "Bahdanau D, Cho K, Bengio Y. Neural machine translation by jointly learning to align and translate. ICLR, 2015.", size: 22 })
                ]
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "[4] ", size: 22 }),
                    new TextRun({ text: "Sutskever I, Vinyals O, Le Q V. Sequence to sequence learning with neural networks. NeurIPS, 2014: 3104-3112.", size: 22 })
                ]
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "[5] ", size: 22 }),
                    new TextRun({ text: "Rush A M, Chopra S, Weston J. A neural attention model for abstractive sentence summarization. EMNLP, 2015: 379-389.", size: 22 })
                ]
            })
        ]
    }]
});

// 保存文档
Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync('/Users/openclaw2026/.qclaw/workspace/demo.docx', buffer);
    console.log('Demo文档已创建: /Users/openclaw2026/.qclaw/workspace/demo.docx');
});
