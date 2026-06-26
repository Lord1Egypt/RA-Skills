"""块属性 - 用于标签和动态字段"""
import ezdxf


class BlockAttributes:
    """图块属性操作"""

    @staticmethod
    def add_attribute(block_layout,
                      tag: str,
                      prompt: str = '',
                      text: str = '',
                      insert_point=(0, 0),
                      height: float = 2.5,
                      layer: str = '0'):
        """
        在块定义中添加属性定义 (ATTDEF)
        Args:
            tag: 属性标签名
            prompt: 输入提示文字
            text: 默认值
        """
        attrib_def = block_layout.add_attdef(
            tag=tag,
            insert=(insert_point[0], insert_point[1], 0),
            height=height,
            dxfattribs={
                'prompt': prompt or f"Enter {tag}",
                'layer': layer,
            }
        )
        return attrib_def

    @staticmethod
    def set_attribute(insert_ref, tag: str, value: str):
        """
        设置插入块的属性值
        
        Args:
            insert_ref: INSERT 实体引用
            tag: 属性标签
            value: 属性值
        """
        try:
            insert_ref.dxf.attribs_follow = True
            # 使用 ATTRIB 实体
            msp = insert_ref.doc().mspace()
            att = msp.add_attrib(
                tag, value,
                insert=insert_ref.dxf.insert,
                dxfattribs={
                    'height': 2.5,
                    'style': 'STANDARD',
                }
            )
            return att
        except Exception as e:
            print(f"[WARN] 设置属性失败: {e}")
            return None
